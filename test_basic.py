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
        
        # List of files to check (some may not be critical for CI/CD)
        files_to_check = {
            'stealth_network_spy_fixed.py': ('Core module', True),  # Must exist
            'main.py': ('Main GUI', True),  # Must exist
            'buildozer.spec': ('Build config', False),  # Optional in CI/CD
            'requirements.txt': ('Dependencies', True)  # Must exist
        }
        
        for filename, (description, required) in files_to_check.items():
            # Check in multiple possible locations
            possible_paths = [
                os.path.join(test_dir, filename),  # Same directory as test
                os.path.join(os.getcwd(), filename),  # Current working directory
                filename  # Relative path
            ]
            
            found = False
            for path in possible_paths:
                if os.path.exists(path):
                    print(f"✅ Found {description}: {filename} at {path}")
                    found = True
                    break
            
            if not found:
                print(f"❌ Missing {description}: {filename}")
                print(f"  Searched in: {possible_paths}")
                print(f"  Test directory: {test_dir}")
                print(f"  Current directory: {os.getcwd()}")
                print(f"  Test directory contents: {os.listdir(test_dir) if os.path.exists(test_dir) else 'N/A'}")
                print(f"  Current directory contents: {os.listdir('.') if os.path.exists('.') else 'N/A'}")
                
                if required:
                    self.fail(f"Required {description} not found: {filename}")
                else:
                    print(f"⚠️ Warning: Optional {description} not found, but continuing...")
        
        # Test file existence doesn't fail the build for optional files
        print("File existence check completed")
    
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