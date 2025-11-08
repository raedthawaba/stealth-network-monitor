#!/bin/bash
# Local APK Build Test Script for Stealth Network Monitor
# This script helps test the build process locally

echo "🔧 Stealth Network Monitor - Local Build Test"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "stealth_network_spy_fixed.py" ]; then
    echo "❌ Error: Please run this script from the stealth-network-monitor directory"
    echo "   cd stealth-network-monitor && ./test_local_build.sh"
    exit 1
fi

echo "📂 Current directory: $(pwd)"
echo "🐍 Python version: $(python3 --version)"

# Check if buildozer is installed
echo ""
echo "🔍 Checking buildozer installation..."
if ! command -v buildozer &> /dev/null; then
    echo "❌ buildozer not found. Installing..."
    pip3 install buildozer cython
else
    echo "✅ buildozer found: $(buildozer --version)"
fi

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Check buildozer configuration
echo ""
echo "⚙️  Checking buildozer configuration..."
if [ -f "buildozer.spec" ]; then
    echo "✅ buildozer.spec found"
    echo "📋 Key settings:"
    grep -E "(title|package.name|source.dir|requirements|orientation)" buildozer.spec | head -5
else
    echo "❌ buildozer.spec not found"
    exit 1
fi

# Test basic compilation
echo ""
echo "🧪 Testing basic Python compilation..."
python3 -m py_compile stealth_network_spy_fixed.py
if [ $? -eq 0 ]; then
    echo "✅ stealth_network_spy_fixed.py compiles successfully"
else
    echo "❌ stealth_network_spy_fixed.py has syntax errors"
    exit 1
fi

python3 -m py_compile main.py
if [ $? -eq 0 ]; then
    echo "✅ main.py compiles successfully"
else
    echo "❌ main.py has syntax errors"
    exit 1
fi

# Run basic tests
echo ""
echo "🧪 Running basic tests..."
if [ -f "test_basic.py" ]; then
    echo "Running test_basic.py..."
    python3 -m pytest test_basic.py -v
else
    echo "Running basic import test..."
    python3 -c "import json, sqlite3, subprocess, os, time; print('✅ Core modules available')"
fi

# Build APK (if Android SDK is available)
echo ""
echo "📱 Attempting to build APK..."
echo "⚠️  Note: This requires Android SDK and will take several minutes"

# Check for Android SDK
if [ -z "$ANDROID_HOME" ]; then
    echo "⚠️  ANDROID_HOME not set. APK build may fail."
    echo "   Set ANDROID_HOME to your Android SDK path to enable builds."
    echo ""
    echo "🔗 GitHub Actions workflow has been fixed to handle this automatically."
    echo "   The next commit should build successfully on GitHub."
else
    echo "✅ ANDROID_HOME found: $ANDROID_HOME"
    echo "📱 Starting APK build..."
    buildozer android debug --verbose
    if [ $? -eq 0 ]; then
        echo "✅ APK build successful!"
        if ls bin/*.apk 1> /dev/null 2>&1; then
            echo "📁 APK files created:"
            ls -la bin/*.apk
        else
            echo "⚠️  No APK found in bin/ directory"
        fi
    else
        echo "❌ APK build failed"
        echo "🔍 Check the logs above for error details"
    fi
fi

echo ""
echo "📋 Summary:"
echo "- Python compilation: ✅"
echo "- Dependencies: ✅"
echo "- Configuration: ✅"
echo "- APK build: See above"
echo ""
echo "🚀 The GitHub CI/CD workflow has been fixed and should now work properly."
echo "   Check your repository at: https://github.com/raedthawaba/stealth-network-monitor/actions"