#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام الرقابة الأبوية للهاتف المحمول - نسخة Termux
Mobile Parental Control System - Termux Version
"""

import os
import json
import sqlite3
import time
import threading
from datetime import datetime, timedelta
import random

class MobileParentalControl:
    def __init__(self):
        self.config = self.load_config()
        self.running = False
        self.setup_database()
    
    def load_config(self):
        """تحميل إعدادات الهاتف"""
        try:
            with open('mobile_config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            # إعدادات افتراضية
            return {
                "mobile_settings": {
                    "stealth_mode": True,
                    "background_monitoring": True
                },
                "children": [
                    {
                        "name": "الطفل الأول",
                        "age": 12,
                        "device_id": "phone_001"
                    }
                ],
                "monitoring_rules": {
                    "blocked_apps": ["instagram", "tiktok", "youtube"],
                    "time_limits": {"weekday": 2, "weekend": 4},
                    "safe_search": True
                }
            }
    
    def setup_database(self):
        """إنشاء قاعدة البيانات"""
        conn = sqlite3.connect('mobile_parental_control.db')
        cursor = conn.cursor()
        
        # جدول الأنشطة
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                child_name TEXT,
                activity_type TEXT,
                content TEXT,
                safety_score INTEGER,
                action_taken TEXT
            )
        ''')
        
        # جدول التطبيقات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                child_name TEXT,
                app_name TEXT,
                duration_minutes INTEGER,
                safety_level TEXT
            )
        ''')
        
        # جدول البحثات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                child_name TEXT,
                search_term TEXT,
                search_engine TEXT,
                safety_level TEXT,
                blocked BOOLEAN
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_activity(self, child_name, activity_type, content, safety_score=100, action=""):
        """تسجيل نشاط"""
        conn = sqlite3.connect('mobile_parental_control.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO activities (timestamp, child_name, activity_type, content, safety_score, action_taken)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), child_name, activity_type, content, safety_score, action))
        
        conn.commit()
        conn.close()
    
    def log_app_usage(self, child_name, app_name, duration, safety_level):
        """تسجيل استخدام التطبيق"""
        conn = sqlite3.connect('mobile_parental_control.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO app_usage (timestamp, child_name, app_name, duration_minutes, safety_level)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), child_name, app_name, duration, safety_level))
        
        conn.commit()
        conn.close()
    
    def log_search(self, child_name, search_term, search_engine, safety_level, blocked=False):
        """تسجيل عملية بحث"""
        conn = sqlite3.connect('mobile_parental_control.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO searches (timestamp, child_name, search_term, search_engine, safety_level, blocked)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), child_name, search_term, search_engine, safety_level, blocked))
        
        conn.commit()
        conn.close()
    
    def check_content_safety(self, content):
        """فحص سلامة المحتوى"""
        # كلمات محظورة
        blocked_keywords = [
            "منتهي", "إباحي", "مؤثر", "قاتل", "عنف", "مخدرات",
            "كحول", "تدخين", "انتحار", "تنمر", "كراهية"
        ]
        
        content_lower = content.lower()
        for keyword in blocked_keywords:
            if keyword in content_lower:
                return "unsafe", 10
        
        # كلمات تحذيرية
        warning_keywords = [
            "لعبة", "فيديو", "موسيقى", "تريلر", "مقاطع"
        ]
        
        for keyword in warning_keywords:
            if keyword in content_lower:
                return "warning", 70
        
        return "safe", 100
    
    def simulate_monitoring(self):
        """محاكاة المراقبة (يمكن استبدالها بالمراقبة الحقيقية)"""
        print("🔍 بدء مراقبة الخلفية...")
        
        # قائمة التطبيقات للاختبار
        apps = [
            ("تطبيق Khan Academy", "safe", 15),
            ("تطبيق Instagram", "warning", 25),
            ("تطبيق YouTube Kids", "safe", 30),
            ("تطبيق TikTok", "unsafe", 20),
            ("تطبيق WhatsApp", "safe", 10),
            ("تطبيق Snapchat", "warning", 15)
        ]
        
        # عمليات البحث للاختبار
        searches = [
            "واجبات مدرسية", "كورس الرياضيات", "ألعاب الأكشن", 
            "مقاطع مضحكة", "البحث عن معلومات", "تعلم البرمجة",
            "محتوى غير مناسب", "أفلام الرعب", "موسيقى شعبية"
        ]
        
        for child in self.config['children']:
            child_name = child['name']
            print(f"\n👶 مراقبة الطفل: {child_name}")
            
            # محاكاة أنشطة عشوائية
            for i in range(5):
                # تطبيق عشوائي
                app_name, app_safety, duration = random.choice(apps)
                self.log_app_usage(child_name, app_name, duration, app_safety)
                
                if app_safety == "unsafe":
                    action = "حجب التطبيق"
                    self.log_activity(child_name, "app_blocked", app_name, 10, action)
                    print(f"🚫 تم حجب: {app_name}")
                else:
                    action = "السماح"
                    self.log_activity(child_name, "app_used", app_name, 80, action)
                    print(f"✅ استخدام: {app_name} لمدة {duration} دقيقة")
                
                time.sleep(1)
                
                # بحث عشوائي
                search_term = random.choice(searches)
                safety_level, safety_score = self.check_content_safety(search_term)
                blocked = safety_level == "unsafe"
                
                self.log_search(child_name, search_term, "Google", safety_level, blocked)
                
                if blocked:
                    action = "حجب البحث"
                    self.log_activity(child_name, "search_blocked", search_term, 10, action)
                    print(f"🚫 تم حجب البحث: {search_term}")
                else:
                    action = "السماح"
                    self.log_activity(child_name, "search_allowed", search_term, 80, action)
                    print(f"✅ البحث المسموح: {search_term}")
                
                time.sleep(1)
    
    def start_background_monitoring(self):
        """بدء المراقبة في الخلفية"""
        self.running = True
        
        def monitor_loop():
            while self.running:
                try:
                    self.simulate_monitoring()
                    # انتظار 30 ثانية قبل المحاكاة التالية
                    time.sleep(30)
                except Exception as e:
                    print(f"خطأ في المراقبة: {e}")
                    time.sleep(10)
        
        # بدء المراقبة في thread منفصل
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
        
        print("🚀 المراقبة بدأت في الخلفية...")
        print("📱 النظام يعمل بصمت - لا يظهر للطفل")
        
        return monitor_thread
    
    def stop_monitoring(self):
        """إيقاف المراقبة"""
        self.running = False
        print("⏹️ تم إيقاف المراقبة")
    
    def generate_report(self):
        """إنشاء تقرير شامل"""
        print("\n" + "="*50)
        print("📊 تقرير الرقابة الأبوية")
        print("="*50)
        
        conn = sqlite3.connect('mobile_parental_control.db')
        cursor = conn.cursor()
        
        # تقرير الأنشطة
        cursor.execute('''
            SELECT child_name, activity_type, content, safety_score, action_taken, timestamp
            FROM activities 
            ORDER BY timestamp DESC
            LIMIT 20
        ''')
        
        activities = cursor.fetchall()
        
        if activities:
            print("\n📝 آخر الأنشطة:")
            for activity in activities:
                print(f"🕐 {activity[5]} - {activity[0]}: {activity[2]} ({activity[3]}/100) - {activity[4]}")
        
        # إحصائيات التطبيقات
        cursor.execute('''
            SELECT child_name, app_name, COUNT(*) as usage_count, AVG(duration_minutes) as avg_duration
            FROM app_usage 
            GROUP BY child_name, app_name
            ORDER BY usage_count DESC
        ''')
        
        app_stats = cursor.fetchall()
        
        if app_stats:
            print("\n📱 إحصائيات التطبيقات:")
            for stat in app_stats:
                print(f"👶 {stat[0]} - {stat[1]}: {stat[2]} مرة, متوسط {stat[3]:.1f} دقيقة")
        
        # إحصائيات البحث
        cursor.execute('''
            SELECT child_name, safety_level, COUNT(*) as count, 
                   SUM(CASE WHEN blocked = 1 THEN 1 ELSE 0 END) as blocked_count
            FROM searches 
            GROUP BY child_name, safety_level
        ''')
        
        search_stats = cursor.fetchall()
        
        if search_stats:
            print("\n🔍 إحصائيات البحث:")
            for stat in search_stats:
                print(f"👶 {stat[0]} - {stat[1]}: {stat[2]} بحث, محجوب: {stat[3]}")
        
        conn.close()
        
        print("\n" + "="*50)
    
    def run_interactive(self):
        """تشغيل تفاعلي"""
        print("🛡️ نظام الرقابة الأبوية للهاتف المحمول")
        print("="*50)
        
        while True:
            print("\nاختر الخيار:")
            print("1. بدء المراقبة في الخلفية")
            print("2. إيقاف المراقبة") 
            print("3. عرض التقرير")
            print("4. محاكاة مراقبة سريعة")
            print("5. خروج")
            
            try:
                choice = input("\nاختيارك (1-5): ").strip()
                
                if choice == "1":
                    self.start_background_monitoring()
                    input("اضغط Enter للمتابعة...")
                
                elif choice == "2":
                    self.stop_monitoring()
                    input("اضغط Enter للمتابعة...")
                
                elif choice == "3":
                    self.generate_report()
                    input("اضغط Enter للمتابعة...")
                
                elif choice == "4":
                    print("🔄 تشغيل محاكاة سريعة...")
                    self.simulate_monitoring()
                    print("✅ انتهت المحاكاة")
                    input("اضغط Enter للمتابعة...")
                
                elif choice == "5":
                    print("👋 goodbye!")
                    self.stop_monitoring()
                    break
                
                else:
                    print("❌ اختيار غير صحيح")
            
            except KeyboardInterrupt:
                print("\n\n⏹️ إيقاف النظام...")
                self.stop_monitoring()
                break

# الاستخدام الرئيسي
if __name__ == "__main__":
    control = MobileParentalControl()
    control.run_interactive()