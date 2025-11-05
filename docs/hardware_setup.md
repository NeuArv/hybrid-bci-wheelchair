# Hardware Setup Guide

This guide provides detailed instructions for setting up the hardware components of the Hybrid BCI Wheelchair system.

## Table of Contents

1. [Bill of Materials](#bill-of-materials)
2. [Raspberry Pi Setup](#raspberry-pi-setup)
3. [Motor Driver Connections](#motor-driver-connections)
4. [Ultrasonic Sensor Connections](#ultrasonic-sensor-connections)
5. [EEG Headset Setup](#eeg-headset-setup)
6. [Power Supply](#power-supply)
7. [Safety Considerations](#safety-considerations)

## Bill of Materials

### Core Components

| Component | Quantity | Specifications | Purpose |
|-----------|----------|----------------|---------|
| Raspberry Pi 3B+ | 1 | 1GB RAM, 40-pin GPIO | Main controller |
| Neurosky Mindwave Mobile 2 | 1 | EEG headset with Bluetooth | Brain signal acquisition |
| L298N Motor Driver | 1 | Dual H-bridge, 2A per channel | Motor control |
| DC Motors | 2 | 12V, suitable for wheelchair | Propulsion |
| HC-SR04 Ultrasonic Sensor | 1 | Range: 2cm - 400cm | Obstacle detection |
| Power Supply | 1 | 12V, 5A minimum | Motor and Pi power |
| Voltage Regulator | 1 | 12V to 5V, 3A | Power Pi from battery |
| Wheelchair Chassis | 1 | With motor mounts | Mechanical platform |

### Additional Materials

- Jumper wires (male-to-female, male-to-male)
- Breadboard or prototyping board
- Mounting brackets for sensors
- Battery holder (for portable operation)
- Emergency stop button (highly recommended)
- Cable ties and mounting hardware

## Raspberry Pi Setup

### 1. Install Operating System

1. Download Raspberry Pi OS (32-bit, Lite or Desktop)
2. Flash to microSD card using Raspberry Pi Imager
3. Insert card into Pi and boot

### 2. Initial Configuration

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3-pip bluetooth bluez bluez-tools

# Enable necessary interfaces
sudo raspi-config
# Enable: SSH, I2C (optional), Serial (optional)
```

### 3. GPIO Pin Reference

The Raspberry Pi 3B+ has 40 GPIO pins. We use the following in **BOARD numbering mode**:

| Pin | Function | Component |
|-----|----------|-----------|
| 3   | GPIO 2   | Motor Right IN1 |
| 5   | GPIO 3   | Motor Right IN2 |
| 7   | GPIO 4   | Motor Right EN (PWM) |
| 8   | GPIO 14  | Ultrasonic TRIG |
| 10  | GPIO 15  | Ultrasonic ECHO |
| 13  | GPIO 27  | Motor Left IN1 |
| 15  | GPIO 22  | Motor Left IN2 |
| 19  | GPIO 10  | Motor Left EN (PWM) |

## Motor Driver Connections

### L298N Motor Driver Pinout

```
L298N Module:
┌─────────────────────┐
│  12V    GND    5V   │  ← Power input
│  OUT1   OUT2        │  ← Motor A
│  OUT3   OUT4        │  ← Motor B
│  IN1 IN2 ENA        │  ← Control A
│  IN3 IN4 ENB        │  ← Control B
└─────────────────────┘
```

### Wiring Table

| L298N Pin | Raspberry Pi Pin | Function |
|-----------|------------------|----------|
| 12V       | 12V Power Supply | Motor power |
| GND       | Pi GND + Power GND | Common ground |
| 5V        | (optional)       | Can power Pi if jumper on |
| ENA       | Pin 7 (GPIO 4)   | Right motor enable (PWM) |
| IN1       | Pin 3 (GPIO 2)   | Right motor direction 1 |
| IN2       | Pin 5 (GPIO 3)   | Right motor direction 2 |
| ENB       | Pin 19 (GPIO 10) | Left motor enable (PWM) |
| IN3       | Pin 13 (GPIO 27) | Left motor direction 1 |
| IN4       | Pin 15 (GPIO 22) | Left motor direction 2 |
| OUT1/OUT2 | Right Motor      | Right motor terminals |
| OUT3/OUT4 | Left Motor       | Left motor terminals |

### Important Notes

1. **Remove the ENA and ENB jumpers** on the L298N module to enable PWM control
2. Ensure common ground between Pi and motor driver
3. Never connect 12V directly to Raspberry Pi pins
4. Test motor direction before mounting on wheelchair

## Ultrasonic Sensor Connections

### HC-SR04 Pinout

```
HC-SR04:
┌───┬───┬───┬───┐
│VCC│TRG│ECH│GND│
└───┴───┴───┴───┘
```

### Wiring Table

| HC-SR04 Pin | Raspberry Pi Pin | Notes |
|-------------|------------------|-------|
| VCC         | Pin 2 (5V)       | Power supply |
| TRIG        | Pin 8 (GPIO 14)  | Trigger signal |
| ECHO        | Pin 10 (GPIO 15) | Echo signal |
| GND         | Pin 6 (GND)      | Ground |

### Voltage Divider for ECHO Pin (Recommended)

The HC-SR04 outputs 5V on ECHO, but Pi GPIO is 3.3V tolerant. Use a voltage divider:

```
ECHO (5V) ─── 1kΩ ───┬─── Pin 10 (GPIO 15)
                     │
                    2kΩ
                     │
                    GND
```

This reduces 5V to ~3.3V for safe operation.

## EEG Headset Setup

### 1. Pairing Neurosky Mindwave Mobile 2

```bash
# Start Bluetooth service
sudo systemctl start bluetooth
sudo systemctl enable bluetooth

# Pair headset
sudo bluetoothctl
[bluetooth]# power on
[bluetooth]# agent on
[bluetooth]# default-agent
[bluetooth]# scan on
# Wait for device to appear: "MindWave Mobile" or similar
# Note the MAC address: XX:XX:XX:XX:XX:XX
[bluetooth]# pair XX:XX:XX:XX:XX:XX
[bluetooth]# trust XX:XX:XX:XX:XX:XX
[bluetooth]# connect XX:XX:XX:XX:XX:XX
[bluetooth]# exit
```

### 2. Create Serial Port Binding

```bash
# Bind to /dev/rfcomm0
sudo rfcomm bind /dev/rfcomm0 XX:XX:XX:XX:XX:XX

# Make persistent (add to /etc/rc.local before 'exit 0'):
sudo nano /etc/rc.local
# Add: rfcomm bind /dev/rfcomm0 XX:XX:XX:XX:XX:XX
```

### 3. Verify Connection

```bash
# Check if device exists
ls -l /dev/rfcomm*

# Test reading data
cat /dev/rfcomm0
# You should see binary data streaming
```

## Power Supply

### Option 1: Bench Power Supply (Testing)

For initial testing, use a bench power supply:
- 12V for motors (via motor driver)
- 5V for Raspberry Pi (via USB or GPIO)

### Option 2: Battery Power (Portable)

For portable operation:

1. **Main Battery**: 12V lead-acid or LiPo (≥5Ah for decent runtime)
2. **Voltage Regulator**: Buck converter 12V → 5V, 3A for Pi
3. **Fuse**: Inline fuse on 12V line (recommended)

```
Battery (12V) ─┬─ Fuse ─ Motor Driver (12V)
               │
               └─ Buck Converter (5V) ─ Raspberry Pi
```

### Power Consumption Estimates

| Component | Current Draw | Power |
|-----------|--------------|-------|
| Raspberry Pi 3B+ | 400-700mA | 2-3.5W |
| Motors (stall) | 2A each | 24W each |
| Motors (running) | 500mA each | 6W each |
| Sensors | <100mA | <0.5W |
| EEG Headset | Battery powered | - |

**Total**: ~20W typical, ~50W peak

## Safety Considerations

### 1. Emergency Stop

**Critical**: Install a physical emergency stop button that cuts motor power.

```
Battery ─ E-Stop Button ─ Motor Driver
```

### 2. Testing Protocol

1. **Test on blocks**: Elevate wheelchair so wheels don't touch ground
2. **Test motors individually**: Verify each motor direction
3. **Test with light load**: Use weights before human testing
4. **Supervise all tests**: Never leave running system unattended
5. **Start slow**: Begin with lowest PWM speed settings

### 3. Electrical Safety

- Use proper gauge wire for motor currents
- Insulate all connections
- Secure all components to prevent shorts
- Add fuses to protect against overcurrent
- Keep water away from electronics

### 4. Software Safety

- Implement timeout: stop motors if no commands received
- Watchdog timer: reset if software hangs
- Battery voltage monitoring: stop if voltage too low
- Signal quality check: stop if EEG signal poor

## Verification Checklist

Before first run:

- [ ] All connections checked against wiring diagrams
- [ ] No short circuits (use multimeter)
- [ ] Motor directions correct (test individually)
- [ ] Ultrasonic sensor working (test with `test_sensors.py`)
- [ ] EEG headset paired and connected
- [ ] Emergency stop button functional
- [ ] All components securely mounted
- [ ] Power supply adequate for load
- [ ] Software tested in simulation mode
- [ ] Supervision available for all tests

## Troubleshooting

### Motors Don't Move

1. Check power supply voltage
2. Verify L298N connections
3. Test with `scripts/test_sensors.py --test motor`
4. Ensure ENA/ENB jumpers removed

### Ultrasonic Returns -1

1. Check sensor connections
2. Verify 5V power
3. Ensure TRIG and ECHO not swapped
4. Add voltage divider if needed

### EEG Not Connecting

1. Verify Bluetooth pairing
2. Check `/dev/rfcomm0` exists
3. Ensure headset battery charged
4. Re-bind RFCOMM port

## Next Steps

After hardware setup:
1. Run hardware tests: `python scripts/test_sensors.py`
2. Calibrate attention threshold
3. Adjust safety distance for obstacles
4. Fine-tune motor speeds
5. Proceed to full system testing

For software setup, see [README.md](../README.md).

