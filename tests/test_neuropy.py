"""
Unit tests for NeuroPy module
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from hybrid_bci.neuropy import NeuroPy


class TestNeuroPy:
    """Test cases for NeuroPy class"""
    
    def test_initialization_default(self):
        """Test NeuroPy initialization with default port"""
        # Don't actually start connection in tests
        neuropy = NeuroPy()
        assert neuropy is not None
    
    def test_initialization_custom_port(self):
        """Test NeuroPy initialization with custom port"""
        neuropy = NeuroPy(port="/dev/rfcomm0", baudRate=57600)
        assert neuropy is not None
    
    def test_callback_registration(self):
        """Test callback function registration"""
        neuropy = NeuroPy()
        
        def test_callback(value):
            pass
        
        neuropy.setCallBack("attention", test_callback)
        assert "attention" in neuropy.callBacksDictionary
    
    def test_property_access(self):
        """Test EEG property access"""
        neuropy = NeuroPy()
        
        # Should return default values without connection
        assert neuropy.attention >= 0
        assert neuropy.meditation >= 0
        assert neuropy.poorSignal >= 0
    
    def test_multiple_callbacks(self):
        """Test multiple callback registrations"""
        neuropy = NeuroPy()
        
        def attention_cb(value):
            pass
        
        def meditation_cb(value):
            pass
        
        neuropy.setCallBack("attention", attention_cb)
        neuropy.setCallBack("meditation", meditation_cb)
        
        assert len(neuropy.callBacksDictionary) == 2

