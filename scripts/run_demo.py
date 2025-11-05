#!/usr/bin/env python
"""
Main Demo Script - Attention-Based Wheelchair Control

This script implements the primary wheelchair control mode using
attention levels from the EEG headset. When attention is above threshold,
the wheelchair moves forward while continuously monitoring for obstacles.

Project Name: Mindwave Automation - Brain Controlled Wheelchair
Author List: Heeral Dedhia, Arvind Sridhar, Poonam Chawda, Arvind Mishra

Usage:
    python scripts/run_demo.py [--port PORT] [--attention-threshold THRESHOLD]
"""

import sys
import time
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from hybrid_bci.neuropy import NeuroPy
from hybrid_bci.motor_control import MotorController
from hybrid_bci.obstacle_detection import ObstacleDetector
from hybrid_bci.blink_detection import BlinkDetector


class AttentionController:
    """
    Main controller for attention-based wheelchair control.
    
    The wheelchair moves forward when attention level exceeds threshold,
    with continuous obstacle monitoring and blink detection for turns.
    """
    
    def __init__(self, port="/dev/rfcomm0", attention_threshold=50):
        """
        Initialize the attention controller.
        
        Args:
            port: Serial port for Neurosky device
            attention_threshold: Minimum attention level to move (0-100)
        """
        self.attention_threshold = attention_threshold
        self.current_attention = 0
        
        print(f"Initializing Hybrid BCI Wheelchair Controller...")
        print(f"Port: {port}")
        print(f"Attention Threshold: {attention_threshold}")
        
        # Initialize components
        self.neuropy = NeuroPy(port)
        self.motor = MotorController()
        self.obstacle_detector = ObstacleDetector()
        self.blink_detector = BlinkDetector(self.neuropy, self.motor)
        
        # Set attention callback
        self.neuropy.setCallBack("attention", self.attention_callback)
    
    def attention_callback(self, attention_value):
        """
        Callback function triggered when attention value is updated.
        
        Args:
            attention_value: Current attention level (0-100)
        """
        self.current_attention = attention_value
        print(f"\nAttention level: {attention_value}")
        
        if attention_value > self.attention_threshold:
            print("Moving forward...")
            self.motor.forward()
            time.sleep(1)
            
            # Check for obstacles
            is_blocked = self.obstacle_detector.monitor_and_stop(
                self.motor,
                blink_callback=self.check_for_blinks
            )
            
        else:
            print("Stopped - Low Attention")
            self.motor.stop()
    
    def check_for_blinks(self):
        """Check for blink commands to change direction"""
        # Run short blink detection check
        result = self.blink_detector.detect_blinks(max_iterations=1000, timeout=2)
        if result:
            print(f"Blink command processed: {result}")
    
    def start(self):
        """Start the wheelchair controller"""
        print("\n=== Starting Hybrid BCI Wheelchair ===")
        print("Connecting to Neurosky headset...")
        print("Please ensure the headset is:")
        print("  1. Powered on")
        print("  2. Firmly touching your forehead")
        print("  3. Bluetooth connected (rfcomm)")
        print("\nPress Ctrl+C to stop\n")
        
        try:
            self.neuropy.start()
            
            # Keep running
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\nStopping controller...")
            self.stop()
        except Exception as e:
            print(f"\nError: {e}")
            self.stop()
    
    def stop(self):
        """Stop the wheelchair controller and cleanup"""
        print("Stopping motors...")
        self.motor.stop()
        
        print("Stopping EEG acquisition...")
        self.neuropy.stop()
        
        print("Cleaning up GPIO...")
        self.motor.cleanup()
        self.obstacle_detector.cleanup()
        
        print("Shutdown complete.")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Hybrid BCI Wheelchair - Attention Control Demo'
    )
    parser.add_argument(
        '--port',
        default='/dev/rfcomm0',
        help='Serial port for Neurosky device (default: /dev/rfcomm0)'
    )
    parser.add_argument(
        '--attention-threshold',
        type=int,
        default=50,
        help='Minimum attention level to move (0-100, default: 50)'
    )
    
    args = parser.parse_args()
    
    controller = AttentionController(
        port=args.port,
        attention_threshold=args.attention_threshold
    )
    controller.start()


if __name__ == '__main__':
    main()

