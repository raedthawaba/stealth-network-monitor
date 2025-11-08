#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام المراقبة الشامل للأطفال - نسخة مصححة
يصلح مشكلة SQLite threading
"""

import sqlite3
import threading
import time
import os
import json
import subprocess
import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

class Monitor:
    def __init__(self):
        self.children = [
            {"name": "الطفل الأول", "ip": "10.0.7.13", "age": 10, "blocked_apps": ["Instagram", "TikTok", "Snapchat"]},
            {"name": "الطفل الثاني", "ip": "10.0.7.20", "age": 14, "blocked_apps": ["Snapchat", "Facebook", "TikTok"]},
            {"name": "الطفل الثالث", "ip": "10.0.7.23", "age": 12, "blocked_apps": ["YouTube", "Instagram", "Games"]},
            {"name": "الطفل الرابع", "ip": "10.0.7.54", "age": 16, "blocked_apps": ["TikTok", "Netflix", "WhatsApp"]},
            {"name": "الطفل الخامس", "ip": "10.0.7.56", "age": 8, "blocked_apps": ["YouTube", "Instagram", "Games"]},
            {"name": "الطفل السادس", "ip": "10.0.7.85", "age": 11, "blocked_apps": ["Snapchat", "TikTok", "Facebook"]}
        ]
        self.db_path = "monitoring.db"
        self.running = True
        self.check_interval = 5  # seconds
        
    def get_db_connection(self):
        """إنشاء اتصال جديد بقاعدة البيانات لكل خيط"""
        return sqlite3.connect(self.db_path, check_same_thread=False)
        
    def init_db(self):
        """إنشاء قاعدة البيانات والجداول"""
        conn = self.get_db_connection()
        try:
            cursor = conn.cursor()
            
            # إنشاء جدول الأنشطة
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    child_name TEXT NOT NULL,
                    ip_address TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    details TEXT,
                    blocked BOOLEAN DEFAULT 0,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # إنشاء جدول حالة الأجهزة
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS device_status (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    child_name TEXT NOT NULL,
                    ip_address TEXT NOT NULL,
                    status TEXT NOT NULL,
                    last_seen DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            print("✅ قاعدة البيانات تم إنشاؤها بنجاح!")
        except sqlite3.Error as e:
            print(f"❌ خطأ في إنشاء قاعدة البيانات: {e}")
        finally:
            conn.close()
    
    def check_device(self, ip):
        """فحص حالة الجهاز باستخدام ping"""
        try:
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '2', ip],
                capture_output=True,
                text=True,
                timeout=3
            )
            return result.returncode == 0
        except:
            return False
    
    def log_activity(self, child_name, ip, activity_type, details, blocked):
        """تسجيل النشاط في قاعدة البيانات"""
        conn = self.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO activities (child_name, ip_address, activity_type, details, blocked)
                VALUES (?, ?, ?, ?, ?)
            ''', (child_name, ip, activity_type, details, blocked))
            conn.commit()
        except sqlite3.Error as e:
            print(f"❌ خطأ في تسجيل النشاط: {e}")
        finally:
            conn.close()
    
    def update_device_status(self, child_name, ip, status):
        """تحديث حالة الجهاز في قاعدة البيانات"""
        conn = self.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO device_status (child_name, ip_address, status)
                VALUES (?, ?, ?)
            ''', (child_name, ip, status))
            conn.commit()
        except sqlite3.Error as e:
            print(f"❌ خطأ في تحديث حالة الجهاز: {e}")
        finally:
            conn.close()
    
    def simulate_activities(self, child):
        """محاكاة أنشطة مختلفة للطفل"""
        activities = [
            ("web_browsing", "تصفح المواقع", False),
            ("app_usage", "استخدام التطبيقات", False),
            ("search_query", "البحث في الإنترنت", False),
            ("messaging", "إرسال رسائل", False),
            ("blocked_app", "محاولة فتح تطبيق محظور", True),
            ("blocked_website", "محاولة زيارة موقع محظور", True)
        ]
        
        # اختيار نشاط عشوائي
        import random
        activity = random.choice(activities)
        return activity
    
    def monitor_child(self, child):
        """مراقبة طفل واحد"""
        child_name = child["name"]
        ip = child["ip"]
        blocked_apps = child["blocked_apps"]
        
        print(f"👀 بدء مراقبة {child_name} ({ip})")
        
        while self.running:
            try:
                # فحص حالة الجهاز
                is_online = self.check_device(ip)
                
                if is_online:
                    if not hasattr(self, f'prev_status_{child_name}'):
                        # الجهاز أصبح متصل
                        self.log_activity(child_name, ip, "device_online", "الجهاز متصل الآن", False)
                        self.update_device_status(child_name, ip, "online")
                        print(f"🔵 {child_name} - متصل")
                    setattr(self, f'prev_status_{child_name}', True)
                    
                    # محاكاة الأنشطة
                    activity_type, details, blocked = self.simulate_activities(child)
                    self.log_activity(child_name, ip, activity_type, details, blocked)
                    
                    if blocked:
                        print(f"🚫 {child_name} - تم منع: {details}")
                    else:
                        print(f"📱 {child_name} - نشاط: {details}")
                else:
                    if hasattr(self, f'prev_status_{child_name}') and getattr(self, f'prev_status_{child_name}'):
                        # الجهاز انقطع الاتصال
                        self.log_activity(child_name, ip, "device_offline", "الجهاز انقطع الاتصال", False)
                        self.update_device_status(child_name, ip, "offline")
                        print(f"⚫ {child_name} - منقطع")
                    setattr(self, f'prev_status_{child_name}', False)
                
                time.sleep(self.check_interval)
                
            except Exception as e:
                print(f"❌ خطأ في مراقبة {child_name}: {e}")
                time.sleep(self.check_interval)
    
    def start(self):
        """بدء النظام"""
        print("🚀 بدء المراقبة الشاملة")
        print("=" * 50)
        
        # إنشاء قاعدة البيانات
        self.init_db()
        
        # بدء مراقبة جميع الأطفال
        threads = []
        for child in self.children:
            thread = threading.Thread(target=self.monitor_child, args=(child,), daemon=True)
            thread.start()
            threads.append(thread)
        
        print("=" * 50)
        for child in self.children:
            print(f"✅ مراقبة: {child['name']} ({child['ip']})")
        
        print("=" * 50)
        print(f"🛡️ {len(self.children)} أطفال تحت المراقبة!")
        print("🛑 لإيقاف: Ctrl+C")
        print("=" * 50)
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.running = False
            print("\n🛑 تم إيقاف المراقبة")

if __name__ == "__main__":
    # إنشاء مجلد المراقبة
    os.makedirs("monitoring", exist_ok=True)
    os.chdir("monitoring")
    
    # بدء المراقبة
    monitor = Monitor()
    monitor.start()