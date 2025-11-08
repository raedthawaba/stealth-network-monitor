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
        # Get the directory where this test file is located
        test_dir = os.path.dirname(os.path.abspath(__file__))
        
        # List of required files to check
        required_files = {
            'stealth_network_spy_fixed.py': 'Main monitoring module not found',
            'main.py': 'Main GUI module not found', 
            'buildozer.spec': 'Buildozer configuration not found',
            'requirements.txt': 'Requirements file not found'
        }
        
        # Check each file
        for filename, error_message in required_files.items():
            file_path = os.path.join(test_dir, filename)
            self.assertTrue(os.path.exists(file_path), error_message)
            
            # Also debug print for CI/CD
            if os.path.exists(file_path):
                print(f"✅ Found: {filename}")
            else:
                print(f"❌ Missing: {filename} at {file_path}")
                print(f"Current test directory: {test_dir}")
                print(f"Directory contents: {os.listdir(test_dir) if os.path.exists(test_dir) else 'Directory not accessible'}")
                break
    
    def test_config_files(self):
        """Test that configuration files are valid"""
        # Get the directory where this test file is located
        test_dir = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(test_dir, 'config.yaml')
        
        if os.path.exists(config_file):
            try:
                import yaml
                with open(config_file, 'r') as f:
                    yaml.safe_load(f)
            except ImportError:
                # YAML not available in this environment, skip
                pass
            except Exception as e:
                self.fail(f"Invalid config.yaml: {e}")

if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)