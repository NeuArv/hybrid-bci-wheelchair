#!/usr/bin/env python
"""
Blink Control Demo

This script demonstrates pure blink-based wheelchair control.
Double blink: Turn right
Triple blink: Turn left

Project Name: Mindwave Automation - Brain Controlled Wheelchair
Author List: Heeral Dedhia, Arvind Sridhar, Poonam Chawda, Arvind Mishra

Usage:
    python scripts/blink_control_demo.py [--port PORT]
"""

import sys
import time
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from hybrid_bci.neuropy import NeuroPy
from hybrid_bci.motor_control import MotorController
from hybrid_bci.blink_detection import BlinkDetector


def main():
    """Main blink control demo"""
    parser = argparse.ArgumentParser(
        description='Hybrid BCI Wheelchair - Blink Control Demo'
    )
    parser.add_argument(
        '--port',
        default='/dev/rfcomm0',
        help='Serial port for Neurosky device (default: /dev/rfcomm0)'
    )
    
    args = parser.parse_args()
    
    print("\n=== Blink Control Demo ===")
    print("Commands:")
    print("  Double blink: Turn right")
    print("  Triple blink: Turn left")
    print("\nConnecting to Neurosky headset...")
    print("Press Ctrl+C to stop\n")
    
    # Initialize components
    neuropy = NeuroPy(args.port)
    motor = MotorController()
    detector = BlinkDetector(neuropy, motor)
    
    try:
        neuropy.start()
        time.sleep(2)  # Allow connection to stabilize
        
        print("Ready! Blink to control the wheelchair.\n")
        
        while True:
            result = detector.detect_blinks(max_iterations=20000, timeout=30)
            if result:
                print(f"Command executed: {result} blink")
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\n\nStopping...")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        motor.stop()
        neuropy.stop()
        motor.cleanup()
        print("Demo complete.")


if __name__ == '__main__':
    main()

