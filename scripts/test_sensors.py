#!/usr/bin/env python
"""
Sensor Testing Script

This script tests the ultrasonic sensor and motor control independently
to verify hardware connections before running the full BCI system.

Usage:
    python scripts/test_sensors.py [--test TYPE]
    
    TYPE can be: motor, ultrasonic, or all (default)
"""

import sys
import time
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from hybrid_bci.motor_control import MotorController
from hybrid_bci.obstacle_detection import ObstacleDetector


def test_motor():
    """Test motor control functions"""
    print("\n=== Motor Control Test ===\n")
    motor = MotorController()
    
    try:
        print("Testing forward motion...")
        motor.forward()
        time.sleep(2)
        motor.stop()
        time.sleep(1)
        
        print("Testing backward motion...")
        motor.backward()
        time.sleep(2)
        motor.stop()
        time.sleep(1)
        
        print("Testing left turn...")
        motor.turn_left()
        time.sleep(2)
        motor.stop()
        time.sleep(1)
        
        print("Testing right turn...")
        motor.turn_right()
        time.sleep(2)
        motor.stop()
        time.sleep(1)
        
        print("Testing speed variations...")
        motor.forward()
        
        print("  Low speed...")
        motor.speed_low()
        time.sleep(2)
        
        print("  Medium speed...")
        motor.speed_medium()
        time.sleep(2)
        
        print("  High speed...")
        motor.speed_high()
        time.sleep(2)
        
        motor.stop()
        
        print("\n✓ Motor test complete!")
        
    except Exception as e:
        print(f"Error during motor test: {e}")
    finally:
        motor.cleanup()


def test_ultrasonic():
    """Test ultrasonic sensor"""
    print("\n=== Ultrasonic Sensor Test ===\n")
    detector = ObstacleDetector()
    
    try:
        print("Taking 10 distance measurements...\n")
        
        for i in range(10):
            distance = detector.measure_distance()
            is_near, _ = detector.is_obstacle_near()
            
            status = "⚠ OBSTACLE" if is_near else "✓ Clear"
            print(f"Measurement {i+1}: {distance:.1f} cm - {status}")
            time.sleep(0.5)
        
        print("\n✓ Ultrasonic sensor test complete!")
        
    except Exception as e:
        print(f"Error during ultrasonic test: {e}")
    finally:
        detector.cleanup()


def test_eeg_connection():
    """Test EEG headset connection"""
    print("\n=== EEG Headset Connection Test ===\n")
    
    try:
        from hybrid_bci.neuropy import NeuroPy
        
        print("Attempting to connect to Neurosky headset...")
        print("Port: /dev/rfcomm0")
        
        neuropy = NeuroPy("/dev/rfcomm0")
        neuropy.start()
        
        print("Waiting for connection...")
        time.sleep(5)
        
        print(f"\nPackets received: {neuropy.packetsReceived}")
        print(f"Attention: {neuropy.attention}")
        print(f"Meditation: {neuropy.meditation}")
        print(f"Poor signal: {neuropy.poorSignal}")
        
        if neuropy.packetsReceived > 0:
            print("\n✓ EEG headset connected successfully!")
        else:
            print("\n⚠ No packets received - check headset connection")
        
        neuropy.stop()
        
    except Exception as e:
        print(f"Error during EEG test: {e}")


def main():
    """Main testing function"""
    parser = argparse.ArgumentParser(
        description='Test hardware components for Hybrid BCI Wheelchair'
    )
    parser.add_argument(
        '--test',
        choices=['motor', 'ultrasonic', 'eeg', 'all'],
        default='all',
        help='Which component to test (default: all)'
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*50)
    print("Hardware Component Testing")
    print("="*50)
    
    try:
        if args.test in ['motor', 'all']:
            test_motor()
        
        if args.test in ['ultrasonic', 'all']:
            test_ultrasonic()
        
        if args.test in ['eeg', 'all']:
            test_eeg_connection()
        
        print("\n" + "="*50)
        print("All tests complete!")
        print("="*50 + "\n")
        
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")


if __name__ == '__main__':
    main()

