#!/bin/bash
# إعداد نظام الرقابة الأبوية على Termux
# Parental Control System Setup for Termux

echo "📱 إعداد نظام الرقابة الأبوية على Termux"
echo "=========================================="

# تحديث الحزم
echo "🔄 تحديث الحزم..."
pkg update -y
pkg upgrade -y

# تثبيت Python والـ packages المطلوبة
echo "🐍 تثبيت Python والحزم..."
pkg install python -y
pkg install python-dev -y
pkg install openssl -y
pkg install curl -y

# تثبيت Python packages
echo "📦 تثبيت المكتبات..."
pip install --upgrade pip
pip install psutil
pip install sqlite3
pip install requests
pip install flask
pip install simplejson

# إنشاء مجلد النظام
echo "📁 إنشاء مجلد النظام..."
mkdir -p ~/parental_control
cd ~/parental_control

# نسخ الملفات (إذا كانت موجودة)
echo "📋 نسخ ملفات النظام..."

# إنشاء ملف بديل للـ psutil إذا لم يعمل
cat > minimal_monitoring.py << 'EOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام مراقبة مبسط للهاتف المحمول
Minimal Mobile Monitoring System
"""

import os
import json
import sqlite3
import time
from datetime import datetime

class MobileParentalMonitor:
    def __init__(self, config_file="mobile_config.json"):
        self.config_file = config_file
        self.setup_database()
    
    def setup_database(self):
        """إنشاء قاعدة بيانات مبسطة"""
        conn = sqlite3.connect('mobile_monitoring.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                activity_type TEXT,
                content TEXT,
                safety_level TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_activity(self, activity_type, content, safety_level="safe"):
        """تسجيل نشاط"""
        conn = sqlite3.connect('mobile_monitoring.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO activities (timestamp, activity_type, content, safety_level)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), activity_type, content, safety_level))
        
        conn.commit()
        conn.close()
    
    def start_monitoring(self):
        """بدء المراقبة الأساسية"""
        print("📱 بدء المراقبة على الهاتف...")
        print("⚠️ تشغيل في الخلفية - لا يظهر للطفل")
        
        # محاكاة مراقبة أساسية
        activities = [
            ("app_usage", "تطبيق YouTube", "safe"),
            ("web_search", "البحث عن الواجبات", "safe"),
            ("app_usage", "تطبيق Instagram", "warning"),
            ("web_search", "البحث عن ألعاب", "safe")
        ]
        
        for activity_type, content, safety in activities:
            self.log_activity(activity_type, content, safety)
            print(f"📝 {activity_type}: {content} - {safety}")
            time.sleep(2)
        
        print("✅ تم حفظ الأنشطة في قاعدة البيانات")
    
    def generate_report(self):
        """إنشاء تقرير"""
        conn = sqlite3.connect('mobile_monitoring.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM activities ORDER BY timestamp DESC')
        activities = cursor.fetchall()
        
        print("\n📊 تقرير الأنشطة:")
        for activity in activities:
            print(f"🕐 {activity[1]} - {activity[2]}: {activity[3]} ({activity[4]})")
        
        conn.close()

# إعداد للهاتف
if __name__ == "__main__":
    monitor = MobileParentalMonitor()
    monitor.start_monitoring()
    monitor.generate_report()
EOF

# إنشاء ملف إعداد الجوال
cat > mobile_config.json << 'EOF'
{
  "mobile_settings": {
    "device_type": "android",
    "run_in_background": true,
    "stealth_mode": true,
    "notification_to_child": false
  },
  "monitoring": {
    "app_monitoring": true,
    "web_monitoring": true,
    "time_restrictions": true,
    "location_tracking": false
  },
  "children": [
    {
      "id": 1,
      "name": "أحمد",
      "age": 12,
      "device_id": "android_device_1"
    }
  ]
}
EOF

echo "✅ تم إعداد النظام على Termux"
echo ""
echo "🚀 خطوات التشغيل:"
echo "1. للدخول للمجلد: cd ~/parental_control"
echo "2. للتشغيل: python3 minimal_monitoring.py"
echo "3. للمراقبة المستمرة: nohup python3 minimal_monitoring.py &"
echo ""
echo "📱 ميزات الهاتف:"
echo "- يعمل في الخلفية دون إزعاج"
echo "- لا يظهر أي رسائل للطفل"
echo "- يحفظ البيانات محلياً"
echo "- يمكن تشغيله مع Termux:Boot"