#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script for Parental Control System
سكريبت تثبيت نظام المراقبة الأبوية
"""

import os
import sys
import subprocess
import json
import platform
from pathlib import Path

def print_banner():
    """طباعة لافتة ترحيبية"""
    print("=" * 60)
    print("🛡️ نظام المراقبة الأبوية المتقدم")
    print("=" * 60)
    print("تم تصميم هذا النظام لحماية الأطفال عبر الإنترنت")
    print("مع احترام خصوصيتهم وتعليمهم السلامة الرقمية")
    print("=" * 60)
    print()

def check_python_version():
    """فحص إصدار Python"""
    print("🔍 فحص إصدار Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ يتطلب Python 3.8 أو أحدث")
        print(f"إصدارك الحالي: {version.major}.{version.minor}")
        print("يرجى تحميل Python من: https://python.org")
        return False
    
    print(f"✅ Python {version.major}.{version.minor} متوافق")
    return True

def check_dependencies():
    """فحص وتثبيت المكتبات المطلوبة"""
    print("\n📦 فحص المكتبات المطلوبة...")
    
    required_packages = [
        'requests',
        'threading',
        'sqlite3'  # included in Python
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'sqlite3':
                import sqlite3
                print(f"✅ {package} متوفر")
            else:
                __import__(package)
                print(f"✅ {package} متوفر")
        except ImportError:
            print(f"❌ {package} غير متوفر")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  سيتم تثبيت المكتبات المفقودة: {', '.join(missing_packages)}")
        return install_packages(missing_packages)
    
    return True

def install_packages(packages):
    """تثبيت المكتبات المفقودة"""
    print("\n🔄 تثبيت المكتبات...")
    
    for package in packages:
        try:
            print(f"تثبيت {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ تم تثبيت {package} بنجاح")
        except subprocess.CalledProcessError:
            print(f"❌ فشل في تثبيت {package}")
            return False
    
    return True

def create_directories():
    """إنشاء المجلدات المطلوبة"""
    print("\n📁 إنشاء المجلدات...")
    
    directories = [
        'logs',
        'reports',
        'backups',
        'exports'
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ تم إنشاء مجلد: {directory}")
        except Exception as e:
            print(f"❌ خطأ في إنشاء مجلد {directory}: {e}")
            return False
    
    return True

def setup_config():
    """إعداد ملف التكوين"""
    print("\n⚙️ إعداد ملف التكوين...")
    
    config_file = 'parental_config.json'
    
    if os.path.exists(config_file):
        print("✅ ملف التكوين موجود بالفعل")
        return True
    
    # إنشاء ملف تكوين افتراضي
    default_config = {
        "system_settings": {
            "network_range": "192.168.1.0/24",
            "scan_interval": 30,
            "log_level": "INFO",
            "database_path": "parental_control.db",
            "log_file": "logs/parental_control.log"
        },
        "children": [
            {
                "id": 1,
                "name": "طفل تجريبي",
                "age_range": "8-12",
                "device_ip": "192.168.1.100",
                "device_type": "كمبيوتر",
                "is_active": False,
                "daily_screen_time_limit": 3
            }
        ],
        "web_filtering": {
            "safe_search_engines": ["google.com/safe", "bing.com/safe"],
            "blocked_domains": [
                "malware.com",
                "phishing.net",
                "adult-content.com"
            ],
            "inappropriate_keywords": [
                "adult", "explicit", "violence", "gambling",
                "drugs", "alcohol", "tobacco", "suicide"
            ]
        },
        "alerts": {
            "notification_methods": {
                "console": True,
                "log_file": True
            },
            "alert_thresholds": {
                "inappropriate_searches": 2,
                "blocked_website_attempts": 3,
                "excessive_screen_time": 4
            }
        }
    }
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        print("✅ تم إنشاء ملف التكوين الافتراضي")
        print(f"📝 يرجى تحرير {config_file} لإضافة أطفالك")
        return True
    except Exception as e:
        print(f"❌ خطأ في إنشاء ملف التكوين: {e}")
        return False

def create_startup_script():
    """إنشاء ملف تشغيل"""
    print("\n🚀 إنشاء ملف التشغيل...")
    
    system = platform.system()
    
    if system == "Windows":
        script_content = """@echo off
title نظام المراقبة الأبوية
cd /d "%~dp0"
python ParentalControlSystem.py
pause
"""
        script_name = "start_parental_control.bat"
    else:  # macOS/Linux
        script_content = """#!/bin/bash
echo "بدء تشغيل نظام المراقبة الأبوية..."
cd "$(dirname "$0")"
python3 ParentalControlSystem.py
read -p "اضغط Enter للمتابعة..."
"""
        script_name = "start_parental_control.sh"
    
    try:
        with open(script_name, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        if system != "Windows":
            os.chmod(script_name, 0o755)
        
        print(f"✅ تم إنشاء ملف التشغيل: {script_name}")
        return True
    except Exception as e:
        print(f"❌ خطأ في إنشاء ملف التشغيل: {e}")
        return False

def check_network_permissions():
    """فحص صلاحيات الشبكة"""
    print("\n🌐 فحص صلاحيات الشبكة...")
    
    system = platform.system()
    
    if system == "Windows":
        print("💡 في Windows، قد تحتاج لتشغيل البرنامج كمدير")
        print("   انقر بالزر الأيمن على الملف واختر 'Run as administrator'")
    else:
        print("💡 في Linux/macOS، قد تحتاج لاستخدام sudo:")
        print("   sudo python ParentalControlSystem.py")
    
    return True

def run_test():
    """تشغيل اختبار النظام"""
    print("\n🧪 تشغيل اختبار النظام...")
    
    try:
        # اختبار استيراد الوحدات
        import sqlite3
        import requests
        import threading
        print("✅ جميع الوحدات تعمل بشكل صحيح")
        
        # اختبار إنشاء قاعدة بيانات
        test_db = "test_installation.db"
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE test (id INTEGER)")
        conn.commit()
        conn.close()
        
        # حذف ملف الاختبار
        os.remove(test_db)
        print("✅ قاعدة البيانات تعمل بشكل صحيح")
        
        return True
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        return False

def print_next_steps():
    """طباعة الخطوات التالية"""
    print("\n" + "=" * 60)
    print("🎉 تم تثبيت النظام بنجاح!")
    print("=" * 60)
    print()
    print("الخطوات التالية:")
    print("1. 📝 حرر ملف 'parental_config.json' لإضافة أطفالك")
    print("2. 🖥️  افتح 'parental_dashboard.html' في متصفح لمشاهدة لوحة التحكم")
    print("3. 🚀 شغل النظام:")
    
    system = platform.system()
    if system == "Windows":
        print("   انقر نقراً مزدوجاً على 'start_parental_control.bat'")
    else:
        print("   ./start_parental_control.sh")
    
    print("   أو: python ParentalControlSystem.py")
    print()
    print("💡 نصائح مهمة:")
    print("   • تحدث مع أطفالك حول الغرض من المراقبة")
    print("   • احترم خصوصيتهم واستخدم البيانات للأمان فقط")
    print("   • راجع INSTALLATION_GUIDE.md للتفاصيل المتقدمة")
    print("   • احترم قوانين الخصوصية في بلدك")
    print()
    print("🛡️ تذكر: الهدف هو الحماية والتوجيه، وليس التجسس!")
    print("=" * 60)

def main():
    """الدالة الرئيسية للتثبيت"""
    print_banner()
    
    # فحص Python
    if not check_python_version():
        input("\nاضغط Enter للخروج...")
        return False
    
    # فحص المكتبات
    if not check_dependencies():
        print("\n❌ فشل في تثبيت المكتبات المطلوبة")
        input("اضغط Enter للخروج...")
        return False
    
    # إنشاء المجلدات
    if not create_directories():
        print("\n❌ فشل في إنشاء المجلدات")
        input("اضغط Enter للخروج...")
        return False
    
    # إعداد التكوين
    if not setup_config():
        print("\n❌ فشل في إعداد التكوين")
        input("اضغط Enter للخروج...")
        return False
    
    # إنشاء ملف التشغيل
    if not create_startup_script():
        print("\n⚠️ تحذير: فشل في إنشاء ملف التشغيل")
        print("يمكنك تشغيل النظام مباشرة باستخدام: python ParentalControlSystem.py")
    
    # فحص صلاحيات الشبكة
    check_network_permissions()
    
    # تشغيل اختبار
    if not run_test():
        print("\n⚠️ تحذير: فشل في اختبار النظام")
        print("قد تحتاج لمراجعة التثبيت")
    
    # طباعة الخطوات التالية
    print_next_steps()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ فشل في التثبيت")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n🛑 تم إيقاف التثبيت بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        sys.exit(1)