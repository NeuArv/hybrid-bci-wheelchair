"""
Hybrid BCI Wheelchair Control System

A brain-computer interface system for wheelchair control using
Neurosky Mindwave EEG headset with attention-based control,
blink detection, and obstacle avoidance.
"""

__version__ = "1.0.0"
__author__ = "Arvind Gyandatt Mishra, Poonam Chawda, Heeral Dedhia, Arvind Sridhar"

from .neuropy import NeuroPy

__all__ = ['NeuroPy', 'motor_control', 'blink_detection', 'obstacle_detection']

