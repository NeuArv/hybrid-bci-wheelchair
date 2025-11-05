"""
NeuroPy Library - Interface for Neurosky Mindwave EEG headset

This module provides a Python interface to communicate with the Neurosky
Mindwave Mobile headset via serial connection.
"""

import serial
import time
import sys
from threading import Thread

# Byte codes
CONNECT = '\xc0'
DISCONNECT = '\xc1'
AUTOCONNECT = '\xc2'
SYNC = '\xaa'
EXCODE = '\x55'
POOR_SIGNAL = '\x02'
ATTENTION = '\x04'
MEDITATION = '\x05'
BLINK = '\x16'
HEADSET_CONNECTED = '\xd0'
HEADSET_NOT_FOUND = '\xd1'
HEADSET_DISCONNECTED = '\xd2'
REQUEST_DENIED = '\xd3'
STANDBY_SCAN = '\xd4'
RAW_VALUE = '\x80'


class NeuroPy(object):
    """NeuroPy library, to get data from neurosky mindwave.
    
    Initialising: object1=NeuroPy("COM6",57600) #windows
    After initialising, if required the callbacks must be set
    then using the start method the library will start fetching data from mindwave
    i.e. object1.start()
    similarly stop method can be called to stop fetching the data
    i.e. object1.stop()

    The data from the device can be obtained using either of the following methods or both of them together:

    Obtaining value: variable1=object1.attention #to get value of attention
    #other variables: attention,meditation,rawValue,delta,theta,lowAlpha,highAlpha,lowBeta,highBeta,lowGamma,midGamma, poorSignal and blinkStrength

    Setting callback: a call back can be associated with all the above variables so that a function is called when the variable is updated.
    Syntax: setCallBack("variable",callback_function)
    for eg. to set a callback for attention data the syntax will be setCallBack("attention",callback_function)
    """
    
    __attention = 0
    __meditation = 0
    __rawValue = 0
    __delta = 0
    __theta = 0
    __lowAlpha = 0
    __highAlpha = 0
    __lowBeta = 0
    __highBeta = 0
    __lowGamma = 0
    __midGamma = 0
    __poorSignal = 0
    __blinkStrength = 0

    callBacksDictionary = {}  # keep a track of all callbacks

    def __init__(self, port=None, baudRate=57600, devid=None):
        if port is None:
            platform = sys.platform
            if platform == "win32":
                port = "COM6"
            elif platform.startswith("linux") or platform == 'darwin':
                port = "/dev/rfcomm0"

        self.__devid = devid
        self.__serialPort = port
        self.__serialBaudRate = baudRate
        self.__packetsReceived = 0

        self.__parserThread = None
        self.__threadRun = False
        self.__srl = None
        self.__connected = False

    def __del__(self):
        if self.__threadRun:
            self.stop()

    def disconnect(self):
        self.__srl.write(DISCONNECT)

    def connect(self):
        if not self.__devid:
            self.__connected = True
            return  # Only connect RF devices

        self.__srl.write(''.join([CONNECT, self.__devid.decode('hex')]))

    def start(self):
        """Start the data collection thread"""
        if self.__threadRun:
            print("Mindwave has already started!")
            return

        if self.__srl is None:
            try:
                self.__srl = serial.Serial(
                    self.__serialPort, self.__serialBaudRate)
            except serial.serialutil.SerialException as e:
                print(str(e))
                return
        else:
            self.__srl.open()

        self.__srl.flushInput()

        if self.__devid:
            self.connect()

        self.__packetsReceived = 0
        self.__parserThread = Thread(target=self.__packetParser, args=())
        self.__threadRun = True
        self.__parserThread.start()

    def __packetParser(self):
        """Packet parser runs continuously in a separate thread to parse packets from mindwave"""
        while self.__threadRun:
            p1 = self.__srl.read(1).encode("hex")
            p2 = self.__srl.read(1).encode("hex")
            while (p1 != 'aa' or p2 != 'aa') and self.__threadRun:
                p1 = p2
                p2 = self.__srl.read(1).encode("hex")
            else:
                if not self.__threadRun:
                    break
                # a valid packet is available
                self.__packetsReceived += 1
                payload = []
                checksum = 0
                payloadLength = int(self.__srl.read(1).encode("hex"), 16)
                for i in range(payloadLength):
                    tempPacket = self.__srl.read(1).encode("hex")
                    payload.append(tempPacket)
                    checksum += int(tempPacket, 16)
                checksum = ~checksum & 0x000000ff
                if checksum == int(self.__srl.read(1).encode("hex"), 16):
                    i = 0

                    while i < payloadLength:
                        code = payload[i]
                        if code == 'd0':
                            print("Headset connected!")
                            self.__connected = True
                        elif code == 'd1':
                            print("Headset not found, reconnecting")
                            self.connect()
                        elif code == 'd2':
                            print("Disconnected!")
                            self.connect()
                        elif code == 'd3':
                            print("Headset denied operation!")
                        elif code == 'd4':
                            if payload[2] == 0 and not self.__connected:
                                print("Idle, trying to reconnect")
                                self.connect()
                        elif code == '02':  # poorSignal
                            i = i + 1
                            self.poorSignal = int(payload[i], 16)
                        elif code == '04':  # attention
                            i = i + 1
                            self.attention = int(payload[i], 16)
                        elif code == '05':  # meditation
                            i = i + 1
                            self.meditation = int(payload[i], 16)
                        elif code == '16':  # blink strength
                            i = i + 1
                            self.blinkStrength = int(payload[i], 16)
                        elif code == '80':  # raw value
                            i = i + 1  # for length
                            i = i + 1
                            val0 = int(payload[i], 16)
                            i = i + 1
                            self.rawValue = val0 * 256 + int(payload[i], 16)
                            if self.rawValue > 32768:
                                self.rawValue = self.rawValue - 65536
                        elif code == '83':  # ASIC_EEG_POWER
                            i = i + 1  # for length
                            # delta:
                            i = i + 1
                            val0 = int(payload[i], 16)
                            i = i + 1
                            val1 = int(payload[i], 16)
                            i = i + 1
                            self.delta = val0 * 65536 + val1 * 256 + int(payload[i], 16)
                            # theta:
                            i = i + 1
                            val0 = int(payload[i], 16)
                            i = i + 1
                            val1 = int(payload[i], 16)
                            i = i + 1
                            self.theta = val0 * 65536 + val1 * 256 + int(payload[i], 16)
                            # lowAlpha:
                            i = i + 1
                            val0 = int(payload[i], 16)
                            i = i + 1
                            val1 = int(payload[i], 16)
                            i = i + 1
                            self.lowAlpha = val0 * 65536 + val1 * 256 + int(payload[i], 16)
                            # highAlpha:
                            i = i + 1
                            val0 = int(payload[i], 16)
                            i = i + 1
                            val1 = int(payload[i], 16)
                            i = i + 1
                            self.highAlpha = val0 * 65536 + val1 * 256 + int(payload[i], 16)
                            # lowBeta:
                            i = i + 1
                            val0 = int(payload[i], 16)
                            i = i + 1
                            val1 = int(payload[i], 16)
                            i = i + 1
                            self.lowBeta = val0 * 65536 + val1 * 256 + int(payload[i], 16)
                            # highBeta:
                            i = i + 1
                            val0 = int(payload[i], 16)
                            i = i + 1
                            val1 = int(payload[i], 16)
                            i = i + 1
                            self.highBeta = val0 * 65536 + val1 * 256 + int(payload[i], 16)
                            # lowGamma:
                            i = i + 1
                            val0 = int(payload[i], 16)
                            i = i + 1
                            val1 = int(payload[i], 16)
                            i = i + 1
                            self.lowGamma = val0 * 65536 + val1 * 256 + int(payload[i], 16)
                            # midGamma:
                            i = i + 1
                            val0 = int(payload[i], 16)
                            i = i + 1
                            val1 = int(payload[i], 16)
                            i = i + 1
                            self.midGamma = val0 * 65536 + val1 * 256 + int(payload[i], 16)
                        else:
                            pass
                        i = i + 1

    def stop(self):
        """Stop the running parser thread"""
        if self.__threadRun:
            self.__threadRun = False
            self.__parserThread.join()
            self.__srl.close()

    def setCallBack(self, variable_name, callback_function):
        """Set callback for a variable.
        
        Args:
            variable_name: Name of the variable to set callback for
            callback_function: Function to call when variable is updated
        """
        self.callBacksDictionary[variable_name] = callback_function

    # Property definitions for all EEG metrics

    @property
    def packetsReceived(self):
        return self.__packetsReceived

    @property
    def bytesAvailable(self):
        if self.__threadRun:
            return self.__srl.inWaiting()
        else:
            return -1

    @property
    def attention(self):
        """Get value for attention"""
        return self.__attention

    @attention.setter
    def attention(self, value):
        self.__attention = value
        if "attention" in self.callBacksDictionary:
            self.callBacksDictionary["attention"](self.__attention)

    @property
    def meditation(self):
        """Get value for meditation"""
        return self.__meditation

    @meditation.setter
    def meditation(self, value):
        self.__meditation = value
        if "meditation" in self.callBacksDictionary:
            self.callBacksDictionary["meditation"](self.__meditation)

    @property
    def rawValue(self):
        """Get value for rawValue"""
        return self.__rawValue

    @rawValue.setter
    def rawValue(self, value):
        self.__rawValue = value
        if "rawValue" in self.callBacksDictionary:
            self.callBacksDictionary["rawValue"](self.__rawValue)

    @property
    def delta(self):
        """Get value for delta"""
        return self.__delta

    @delta.setter
    def delta(self, value):
        self.__delta = value
        if "delta" in self.callBacksDictionary:
            self.callBacksDictionary["delta"](self.__delta)

    @property
    def theta(self):
        """Get value for theta"""
        return self.__theta

    @theta.setter
    def theta(self, value):
        self.__theta = value
        if "theta" in self.callBacksDictionary:
            self.callBacksDictionary["theta"](self.__theta)

    @property
    def lowAlpha(self):
        """Get value for lowAlpha"""
        return self.__lowAlpha

    @lowAlpha.setter
    def lowAlpha(self, value):
        self.__lowAlpha = value
        if "lowAlpha" in self.callBacksDictionary:
            self.callBacksDictionary["lowAlpha"](self.__lowAlpha)

    @property
    def highAlpha(self):
        """Get value for highAlpha"""
        return self.__highAlpha

    @highAlpha.setter
    def highAlpha(self, value):
        self.__highAlpha = value
        if "highAlpha" in self.callBacksDictionary:
            self.callBacksDictionary["highAlpha"](self.__highAlpha)

    @property
    def lowBeta(self):
        """Get value for lowBeta"""
        return self.__lowBeta

    @lowBeta.setter
    def lowBeta(self, value):
        self.__lowBeta = value
        if "lowBeta" in self.callBacksDictionary:
            self.callBacksDictionary["lowBeta"](self.__lowBeta)

    @property
    def highBeta(self):
        """Get value for highBeta"""
        return self.__highBeta

    @highBeta.setter
    def highBeta(self, value):
        self.__highBeta = value
        if "highBeta" in self.callBacksDictionary:
            self.callBacksDictionary["highBeta"](self.__highBeta)

    @property
    def lowGamma(self):
        """Get value for lowGamma"""
        return self.__lowGamma

    @lowGamma.setter
    def lowGamma(self, value):
        self.__lowGamma = value
        if "lowGamma" in self.callBacksDictionary:
            self.callBacksDictionary["lowGamma"](self.__lowGamma)

    @property
    def midGamma(self):
        """Get value for midGamma"""
        return self.__midGamma

    @midGamma.setter
    def midGamma(self, value):
        self.__midGamma = value
        if "midGamma" in self.callBacksDictionary:
            self.callBacksDictionary["midGamma"](self.__midGamma)

    @property
    def poorSignal(self):
        """Get value for poorSignal"""
        return self.__poorSignal

    @poorSignal.setter
    def poorSignal(self, value):
        self.__poorSignal = value
        if "poorSignal" in self.callBacksDictionary:
            self.callBacksDictionary["poorSignal"](self.__poorSignal)

    @property
    def blinkStrength(self):
        """Get value for blinkStrength"""
        return self.__blinkStrength

    @blinkStrength.setter
    def blinkStrength(self, value):
        self.__blinkStrength = value
        if "blinkStrength" in self.callBacksDictionary:
            self.callBacksDictionary["blinkStrength"](self.__blinkStrength)

