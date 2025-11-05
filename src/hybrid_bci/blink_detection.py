"""
Blink Detection Module

This module detects eye blinks from EEG raw signals and classifies them
as single, double, or triple blinks for wheelchair control commands.

Project Name: Mindwave Automation - Brain Controlled Wheelchair
"""

import time
from .neuropy import NeuroPy
from . import motor_control


class BlinkDetector:
    """
    Detects blinks from EEG raw values and triggers motor control actions.
    
    Single blink: No action
    Double blink: Turn right
    Triple blink: Turn left
    """
    
    def __init__(self, 
                 neuropy_instance,
                 motor_controller=None,
                 spike_threshold_high=100,
                 spike_threshold_low=-100,
                 blink_duration_min=0.01,
                 blink_duration_max=0.050,
                 multi_blink_window=0.6):
        """
        Initialize blink detector.
        
        Args:
            neuropy_instance: NeuroPy object for EEG data
            motor_controller: MotorController instance (optional)
            spike_threshold_high: Threshold for detecting spike start
            spike_threshold_low: Threshold for detecting spike end
            blink_duration_min: Minimum duration for valid blink (seconds)
            blink_duration_max: Maximum duration for valid blink (seconds)
            multi_blink_window: Time window for detecting multiple blinks (seconds)
        """
        self.neuropy = neuropy_instance
        self.motor = motor_controller
        
        self.spike_threshold_high = spike_threshold_high
        self.spike_threshold_low = spike_threshold_low
        self.blink_duration_min = blink_duration_min
        self.blink_duration_max = blink_duration_max
        self.multi_blink_window = multi_blink_window
        
        self.reset_state()
    
    def reset_state(self):
        """Reset detector state"""
        self.start_time = 0
        self.last_blink_time = 0
        self.blinked = False
        self.double_blink = False
        self.triple_blink = False
    
    def detect_blinks(self, max_iterations=20000, timeout=60):
        """
        Main blink detection loop.
        
        Args:
            max_iterations: Maximum number of samples to process
            timeout: Maximum time to run detection (seconds)
        
        Returns:
            str: Type of blink detected ('single', 'double', 'triple', or None)
        """
        self.reset_state()
        start_loop_time = time.time()
        
        for i in range(max_iterations):
            if time.time() - start_loop_time > timeout:
                print("Blink detection timeout")
                break
            
            value = self.neuropy.rawValue
            
            # Detect spike start
            if value > self.spike_threshold_high:
                self.start_time = time.time()
            
            # Detect spike end and measure duration
            if self.start_time:
                if value < self.spike_threshold_low:
                    total_time = time.time() - self.start_time
                    self.start_time = 0
                    
                    # Check if duration matches a blink
                    if self.blink_duration_min < total_time < self.blink_duration_max:
                        current_time = time.time()
                        
                        # Check if this is part of a multi-blink sequence
                        if self.last_blink_time and \
                           current_time - self.last_blink_time < self.multi_blink_window:
                            if self.double_blink:
                                self.triple_blink = True
                            else:
                                self.double_blink = True
                        
                        self.last_blink_time = current_time
                        self.blinked = True
            
            # Process completed blink sequence
            if self.blinked and time.time() - self.last_blink_time > self.multi_blink_window:
                result = self._process_blink_command()
                self.reset_state()
                return result
            
            time.sleep(0.001)  # Small delay to prevent CPU overload
        
        return None
    
    def _process_blink_command(self):
        """Process the detected blink command and trigger motor action"""
        if self.triple_blink:
            print("Triple blink detected -> Turning left")
            if self.motor:
                self.motor.turn_left()
                time.sleep(3)
                self.motor.forward()
            else:
                motor_control.forward_left()
                time.sleep(3)
                motor_control.forward()
            return 'triple'
        
        elif self.double_blink:
            print("Double blink detected -> Turning right")
            if self.motor:
                self.motor.turn_right()
                time.sleep(3)
                self.motor.forward()
            else:
                motor_control.forward_right()
                time.sleep(3)
                motor_control.forward()
            return 'double'
        
        else:
            print("Single blink detected -> No action")
            return 'single'


def run_blink_detection(port="/dev/rfcomm0", duration=60):
    """
    Convenience function to run blink detection.
    
    Args:
        port: Serial port for Neurosky device
        duration: Maximum duration to run detection (seconds)
    
    Returns:
        str: Type of blink detected
    """
    neuropy = NeuroPy(port)
    neuropy.start()
    
    try:
        detector = BlinkDetector(neuropy)
        result = detector.detect_blinks(timeout=duration)
        return result
    finally:
        neuropy.stop()


