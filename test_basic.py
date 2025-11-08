#!/usr/bin/env python3
"""
Basic tests for Stealth Network Monitor
Simple test suite to validate core functionality
"""

import unittest
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

class TestBasicFunctionality(unittest.TestCase):
    """Basic functionality tests"""
    
    def test_python_version(self):
        """Test that we're running on Python 3.7+"""
        self.assertGreaterEqual(sys.version_info, (3, 7))
    
    def test_core_modules_available(self):
        """Test that core Python modules are available"""
        try:
            import json
            import sqlite3
            import subprocess
            import os
            import time
            import threading
            import hashlib
            import base64
        except ImportError as e:
            self.fail(f"Core module import failed: {e}")
    
    def test_main_files_exist(self):
        """Test that main application files exist"""
        self.assertTrue(os.path.exists('stealth_network_spy_fixed.py'), 
                       "Main monitoring module not found")
        self.assertTrue(os.path.exists('main.py'), 
                       "Main GUI module not found")
        self.assertTrue(os.path.exists('buildozer.spec'), 
                       "Buildozer configuration not found")
        self.assertTrue(os.path.exists('requirements.txt'), 
                       "Requirements file not found")
    
    def test_config_files(self):
        """Test that configuration files are valid"""
        if os.path.exists('config.yaml'):
            try:
                import yaml
                with open('config.yaml', 'r') as f:
                    yaml.safe_load(f)
            except ImportError:
                # YAML not available in this environment, skip
                pass
            except Exception as e:
                self.fail(f"Invalid config.yaml: {e}")

if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)