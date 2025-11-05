"""
Unit tests for motor control module
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from hybrid_bci.motor_control import MotorController


class TestMotorController:
    """Test cases for MotorController class"""
    
    def test_initialization(self):
        """Test motor controller initialization"""
        motor = MotorController()
        assert motor is not None
        assert motor.default_speed == 85
    
    def test_forward_command(self):
        """Test forward motion command"""
        motor = MotorController()
        # Should not raise exception even without GPIO
        motor.forward()
        motor.stop()
    
    def test_backward_command(self):
        """Test backward motion command"""
        motor = MotorController()
        motor.backward()
        motor.stop()
    
    def test_turn_left_command(self):
        """Test left turn command"""
        motor = MotorController()
        motor.turn_left()
        motor.stop()
    
    def test_turn_right_command(self):
        """Test right turn command"""
        motor = MotorController()
        motor.turn_right()
        motor.stop()
    
    def test_speed_settings(self):
        """Test speed control"""
        motor = MotorController()
        motor.speed_low()
        motor.speed_medium()
        motor.speed_high()
        motor.set_speed(50)
    
    def test_cleanup(self):
        """Test cleanup method"""
        motor = MotorController()
        motor.cleanup()
        # Should complete without error


class TestLegacyAPI:
    """Test backward compatibility with legacy function API"""
    
    def test_legacy_forward(self):
        """Test legacy forward function"""
        from hybrid_bci import motor_control
        motor_control.forward()
        motor_control.stop()
    
    def test_legacy_turns(self):
        """Test legacy turn functions"""
        from hybrid_bci import motor_control
        motor_control.forward_left()
        motor_control.forward_right()
        motor_control.stop()
    
    def test_legacy_speed(self):
        """Test legacy speed functions"""
        from hybrid_bci import motor_control
        motor_control.speed_low()
        motor_control.speed_medium()
        motor_control.speed_high()

