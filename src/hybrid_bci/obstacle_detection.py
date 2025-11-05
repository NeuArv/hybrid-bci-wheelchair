"""
Obstacle Detection Module

This module uses an ultrasonic sensor to detect obstacles and prevent
collisions by stopping the wheelchair when objects are too close.

Project Name: Mindwave Automation - Brain Controlled Wheelchair
"""

import time

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except (ImportError, RuntimeError):
    GPIO_AVAILABLE = False
    print("Warning: RPi.GPIO not available. Running in simulation mode.")


class ObstacleDetector:
    """
    Ultrasonic sensor-based obstacle detection for wheelchair safety.
    
    Uses HC-SR04 or similar ultrasonic sensor to measure distance to
    nearest obstacle and trigger safety stop when too close.
    """
    
    def __init__(self,
                 trig_pin=8,
                 echo_pin=10,
                 safety_distance_cm=20,
                 speed_of_sound=343):
        """
        Initialize obstacle detector.
        
        Args:
            trig_pin: GPIO pin for trigger signal
            echo_pin: GPIO pin for echo signal
            safety_distance_cm: Minimum safe distance in centimeters
            speed_of_sound: Speed of sound in m/s (default 343 m/s)
        """
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.safety_distance = safety_distance_cm
        self.speed_of_sound = speed_of_sound
        
        if GPIO_AVAILABLE:
            self._setup_gpio()
    
    def _setup_gpio(self):
        """Initialize GPIO pins for ultrasonic sensor"""
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        
        # Ensure trigger is low
        GPIO.output(self.trig_pin, GPIO.LOW)
        time.sleep(0.1)
    
    def measure_distance(self):
        """
        Measure distance to nearest obstacle.
        
        Returns:
            float: Distance in centimeters, or -1 if measurement fails
        """
        if not GPIO_AVAILABLE:
            # Simulation mode - return safe distance
            return self.safety_distance + 10
        
        try:
            # Send trigger pulse
            GPIO.output(self.trig_pin, GPIO.HIGH)
            time.sleep(0.0001)  # 10 microsecond pulse
            GPIO.output(self.trig_pin, GPIO.LOW)
            
            # Wait for echo start
            timeout_start = time.time()
            while GPIO.input(self.echo_pin) == 0:
                t1 = time.time()
                if t1 - timeout_start > 0.1:  # 100ms timeout
                    return -1
            
            # Wait for echo end
            timeout_start = time.time()
            while GPIO.input(self.echo_pin) == 1:
                t2 = time.time()
                if t2 - timeout_start > 0.1:  # 100ms timeout
                    return -1
            
            # Calculate distance
            # Distance = (time * speed_of_sound) / 2
            # Convert to cm: * 100, speed in m/s
            distance = (t2 - t1) * self.speed_of_sound * 100 / 2
            
            return distance
            
        except Exception as e:
            print(f"Error measuring distance: {e}")
            return -1
    
    def is_obstacle_near(self):
        """
        Check if obstacle is within safety distance.
        
        Returns:
            tuple: (is_near, distance) where is_near is bool and distance is float
        """
        distance = self.measure_distance()
        
        if distance < 0:
            # Measurement failed, assume safe
            return False, distance
        
        is_near = distance < self.safety_distance
        return is_near, distance
    
    def monitor_and_stop(self, motor_controller, blink_callback=None):
        """
        Monitor for obstacles and stop motor if too close.
        
        Args:
            motor_controller: MotorController instance to stop if needed
            blink_callback: Optional callback function for blink detection
            
        Returns:
            bool: True if obstacle detected and stopped, False if safe
        """
        is_near, distance = self.is_obstacle_near()
        
        if is_near:
            motor_controller.stop()
            print(f"OBSTACLE DETECTED! Distance: {distance:.1f} cm - STOPPED")
            time.sleep(2)
            return True
        else:
            print(f"Path clear - Distance: {distance:.1f} cm")
            if blink_callback:
                blink_callback()
            return False
    
    def cleanup(self):
        """Clean up GPIO resources"""
        if GPIO_AVAILABLE:
            GPIO.cleanup()


# Legacy function interface for backward compatibility
_default_detector = None

def _get_detector():
    """Get or create default obstacle detector instance"""
    global _default_detector
    if _default_detector is None:
        _default_detector = ObstacleDetector()
    return _default_detector


def measure_distance():
    """Measure distance to nearest obstacle"""
    return _get_detector().measure_distance()


def check_obstacle(motor_instance=None, blink_callback=None):
    """
    Check for obstacles and take action.
    
    Args:
        motor_instance: Motor controller instance
        blink_callback: Function to call when path is clear
    """
    from . import motor_control
    
    detector = _get_detector()
    is_near, distance = detector.is_obstacle_near()
    
    if is_near:
        if motor_instance:
            motor_instance.stop()
        else:
            motor_control.stop()
        print(f"Stopped - Obstacle Too Close (Distance: {distance:.1f} cm)")
        time.sleep(2)
    else:
        print(f"Moving Forward - Distance: {distance:.1f} cm")
        if blink_callback:
            blink_callback()


