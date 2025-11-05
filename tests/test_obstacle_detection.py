"""
Unit tests for obstacle detection module
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from hybrid_bci.obstacle_detection import ObstacleDetector


class TestObstacleDetector:
    """Test cases for ObstacleDetector class"""
    
    def test_initialization(self):
        """Test obstacle detector initialization"""
        detector = ObstacleDetector()
        assert detector is not None
        assert detector.safety_distance == 20
    
    def test_custom_safety_distance(self):
        """Test custom safety distance setting"""
        detector = ObstacleDetector(safety_distance_cm=30)
        assert detector.safety_distance == 30
    
    def test_measure_distance(self):
        """Test distance measurement"""
        detector = ObstacleDetector()
        distance = detector.measure_distance()
        # In simulation mode, should return safe distance
        assert distance >= 0 or distance == -1
    
    def test_is_obstacle_near(self):
        """Test obstacle proximity check"""
        detector = ObstacleDetector()
        is_near, distance = detector.is_obstacle_near()
        assert isinstance(is_near, bool)
        assert isinstance(distance, (int, float))
    
    def test_cleanup(self):
        """Test cleanup method"""
        detector = ObstacleDetector()
        detector.cleanup()
        # Should complete without error


class TestLegacyAPI:
    """Test backward compatibility with legacy function API"""
    
    def test_legacy_measure_distance(self):
        """Test legacy measure_distance function"""
        from hybrid_bci import obstacle_detection
        distance = obstacle_detection.measure_distance()
        assert isinstance(distance, (int, float))

