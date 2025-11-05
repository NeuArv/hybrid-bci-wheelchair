"""
Motor Control Module

This module handles the motor control for the wheelchair using GPIO pins
on Raspberry Pi. It controls two DC motors via a motor driver for forward,
backward, turning, and speed control.

Project Name: Mindwave Automation - Brain Controlled Wheelchair
"""

import time

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except (ImportError, RuntimeError):
    GPIO_AVAILABLE = False
    print("Warning: RPi.GPIO not available. Running in simulation mode.")


class MotorController:
    """
    Motor controller for wheelchair with dual DC motors.
    
    Attributes:
        inR1, inR2: Right motor direction pins
        enR: Right motor enable pin (PWM)
        inL1, inL2: Left motor direction pins
        enL: Left motor enable pin (PWM)
    """
    
    def __init__(self, 
                 right_pins=(3, 5, 7),
                 left_pins=(13, 15, 19),
                 pwm_frequency=1000,
                 default_speed=85):
        """
        Initialize motor controller.
        
        Args:
            right_pins: Tuple of (inR1, inR2, enR) GPIO pin numbers
            left_pins: Tuple of (inL1, inL2, enL) GPIO pin numbers
            pwm_frequency: PWM frequency in Hz
            default_speed: Default PWM duty cycle (0-100)
        """
        self.inR1, self.inR2, self.enR = right_pins
        self.inL1, self.inL2, self.enL = left_pins
        self.pwm_frequency = pwm_frequency
        self.default_speed = default_speed
        self.pwm_right = None
        self.pwm_left = None
        
        if GPIO_AVAILABLE:
            self._setup_gpio()
    
    def _setup_gpio(self):
        """Initialize GPIO pins and PWM"""
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        
        # Setup all pins as output
        GPIO.setup(self.inR1, GPIO.OUT)
        GPIO.setup(self.inR2, GPIO.OUT)
        GPIO.setup(self.enR, GPIO.OUT)
        GPIO.setup(self.inL1, GPIO.OUT)
        GPIO.setup(self.inL2, GPIO.OUT)
        GPIO.setup(self.enL, GPIO.OUT)
        
        # Initialize all to LOW
        GPIO.output(self.inR1, GPIO.LOW)
        GPIO.output(self.inR2, GPIO.LOW)
        GPIO.output(self.inL1, GPIO.LOW)
        GPIO.output(self.inL2, GPIO.LOW)
        
        # Setup PWM
        self.pwm_right = GPIO.PWM(self.enR, self.pwm_frequency)
        self.pwm_left = GPIO.PWM(self.enL, self.pwm_frequency)
        
        # Start PWM with default speed
        self.pwm_right.start(self.default_speed)
        self.pwm_left.start(self.default_speed)
    
    def forward(self):
        """Move wheelchair forward"""
        if GPIO_AVAILABLE:
            GPIO.output(self.inR1, 0)
            GPIO.output(self.inR2, 1)
            GPIO.output(self.inL1, 0)
            GPIO.output(self.inL2, 1)
        print("Motor: Forward")
    
    def backward(self):
        """Move wheelchair backward"""
        if GPIO_AVAILABLE:
            GPIO.output(self.inR1, 1)
            GPIO.output(self.inR2, 0)
            GPIO.output(self.inL1, 1)
            GPIO.output(self.inL2, 0)
        print("Motor: Backward")
    
    def turn_left(self):
        """Turn wheelchair left (right motor on, left motor off)"""
        if GPIO_AVAILABLE:
            GPIO.output(self.inR1, 0)
            GPIO.output(self.inR2, 0)
            GPIO.output(self.inL1, 0)
            GPIO.output(self.inL2, 1)
        print("Motor: Turning left")
    
    def turn_right(self):
        """Turn wheelchair right (left motor on, right motor off)"""
        if GPIO_AVAILABLE:
            GPIO.output(self.inR1, 0)
            GPIO.output(self.inR2, 1)
            GPIO.output(self.inL1, 0)
            GPIO.output(self.inL2, 0)
        print("Motor: Turning right")
    
    def stop(self):
        """Stop all motors"""
        if GPIO_AVAILABLE:
            GPIO.output(self.inR1, 0)
            GPIO.output(self.inR2, 0)
            GPIO.output(self.inL1, 0)
            GPIO.output(self.inL2, 0)
        print("Motor: Stopped")
    
    def set_speed(self, speed):
        """
        Set motor speed using PWM duty cycle.
        
        Args:
            speed: PWM duty cycle (0-100)
        """
        if GPIO_AVAILABLE and self.pwm_right and self.pwm_left:
            self.pwm_right.ChangeDutyCycle(speed)
            self.pwm_left.ChangeDutyCycle(speed)
        print(f"Motor: Speed set to {speed}%")
    
    def speed_low(self):
        """Set low speed (15% duty cycle)"""
        self.set_speed(15)
    
    def speed_medium(self):
        """Set medium speed (40% duty cycle)"""
        self.set_speed(40)
    
    def speed_high(self):
        """Set high speed (80% duty cycle)"""
        self.set_speed(80)
    
    def cleanup(self):
        """Clean up GPIO resources"""
        if GPIO_AVAILABLE:
            self.stop()
            if self.pwm_right:
                self.pwm_right.stop()
            if self.pwm_left:
                self.pwm_left.stop()
            GPIO.cleanup()


# Legacy function interface for backward compatibility
_default_controller = None

def _get_controller():
    """Get or create default motor controller instance"""
    global _default_controller
    if _default_controller is None:
        _default_controller = MotorController()
    return _default_controller


def forward():
    """Move wheelchair forward"""
    _get_controller().forward()


def backward():
    """Move wheelchair backward"""
    _get_controller().backward()


def forward_left():
    """Turn wheelchair left"""
    _get_controller().turn_left()


def forward_right():
    """Turn wheelchair right"""
    _get_controller().turn_right()


def stop():
    """Stop all motors"""
    _get_controller().stop()


def speed_low():
    """Set low speed"""
    _get_controller().speed_low()


def speed_medium():
    """Set medium speed"""
    _get_controller().speed_medium()


def speed_high():
    """Set high speed"""
    _get_controller().speed_high()


