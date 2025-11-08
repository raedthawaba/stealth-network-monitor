#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام الرقابة الأبوية المبسط للهاتف
Simple Mobile Parental Control System
"""

import os
import json
import sqlite3
import time
import threading
from datetime import datetime
import random

def print_arabic(text):
    """طباعة النص العربي"""
    try:
        print(text)
    except:
        # fallback للترميز
        print(text.encode('utf-8', errors='ignore').decode('utf-8'))

class SimpleMobileParental:
    def __init__(self):
        self.config = self.load_config()
        self.running = False
        self.setup_database()
    
    def load_config(self):
        """تحميل إعدادات"""
        try:
            with open('mobile_config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            # إعدادات افتراضية بسيطة
            return {
                "children": [
                    {"name": "الطفل الأول", "age": 12},
                    {"name": "الطفل الثاني", "age": 9}
                ],
                "blocked_apps": ["instagram", "tiktok", "snapchat"],
                "blocked_keywords": ["منتهي", "إباحي", "عنف"]
            }
    
    def setup_database(self):
        """إنشاء قاعدة البيانات"""
        conn = sqlite3.connect('mobile_monitoring.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                child_name TEXT,
                activity TEXT,
                status TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_activity(self, child_name, activity, status):
        """تسجيل نشاط"""
        conn = sqlite3.connect('mobile_monitoring.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO activities (timestamp, child_name, activity, status)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), child_name, activity, status))
        
        conn.commit()
        conn.close()
    
    def check_safety(self, content):
        """فحص سلامة المحتوى"""
        content_lower = content.lower()
        
        # فحص الكلمات المحظورة
        for keyword in self.config.get("blocked_keywords", []):
            if keyword in content_lower:
                return "blocked", f"محتوى محظور: {keyword}"
        
        # فحص التطبيقات المحظورة  
        for app in self.config.get("blocked_apps", []):
            if app.lower() in content_lower:
                return "blocked", f"تطبيق محظور: {app}"
        
        return "allowed", "آمن"
    
    def simulate_monitoring(self):
        """محاكاة المراقبة"""
        print_arabic("🔍 بدء مراقبة الأطفال...")
        
        # أنشطة محاكاة
        activities = [
            "استخدام تطبيق Khan Academy", 
            "البحث عن الواجبات المدرسية",
            "استخدام تطبيق Instagram", 
            "البحث عن ألعاب الأكشن",
            "استخدام تطبيق TikTok",
            "البحث عن محتوى تعليمي"
        ]
        
        for child in self.config.get("children", []):
            child_name = child.get("name", "طفل")
            print_arabic(f"\n👶 مراقبة: {child_name}")
            
            for i in range(3):
                activity = random.choice(activities)
                status, message = self.check_safety(activity)
                
                if status == "blocked":
                    print_arabic(f"🚫 {child_name}: {message}")
                    self.log_activity(child_name, activity, "محظور")
                else:
                    print_arabic(f"✅ {child_name}: {activity} - {message}")
                    self.log_activity(child_name, activity, "مسموح")
                
                time.sleep(1)
    
    def show_report(self):
        """عرض التقرير"""
        print_arabic("\n" + "="*50)
        print_arabic("📊 تقرير المراقبة")
        print_arabic("="*50)
        
        conn = sqlite3.connect('mobile_monitoring.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM activities ORDER BY timestamp DESC LIMIT 10')
        records = cursor.fetchall()
        
        if records:
            for record in records:
                timestamp = record[1]
                child = record[2] 
                activity = record[3]
                status = record[4]
                
                if status == "محظور":
                    print_arabic(f"🚫 {timestamp} - {child}: {activity}")
                else:
                    print_arabic(f"✅ {timestamp} - {child}: {activity}")
        else:
            print_arabic("❌ لا توجد أنشطة مسجلة")
        
        conn.close()
        print_arabic("="*50)
    
    def start_background(self):
        """بدء المراقبة في الخلفية"""
        self.running = True
        
        def monitor_loop():
            while self.running:
                try:
                    self.simulate_monitoring()
                    time.sleep(60)  # كل دقيقة
                except Exception as e:
                    print_arabic(f"خطأ: {e}")
                    time.sleep(10)
        
        thread = threading.Thread(target=monitor_loop, daemon=True)
        thread.start()
        
        print_arabic("🚀 المراقبة بدأت في الخلفية")
        print_arabic("📱 يعمل بصمت - لا يراه الطفل")
    
    def stop_monitoring(self):
        """إيقاف المراقبة"""
        self.running = False
        print_arabic("⏹️ تم إيقاف المراقبة")
    
    def run_menu(self):
        """قائمة التفاعل"""
        print_arabic("🛡️ نظام الرقابة الأبوية المبسط")
        print_arabic("="*50)
        
        while True:
            print_arabic("\nاختر:")
            print_arabic("1. بدء مراقبة سريعة")
            print_arabic("2. بدء مراقبة خلفية")
            print_arabic("3. إيقاف المراقبة")
            print_arabic("4. عرض التقرير")
            print_arabic("5. خروج")
            
            try:
                choice = input("\nاختيارك (1-5): ").strip()
                
                if choice == "1":
                    print_arabic("\n🔄 تشغيل مراقبة سريعة...")
                    self.simulate_monitoring()
                    input("\nاضغط Enter للمتابعة...")
                
                elif choice == "2":
                    self.start_background()
                    input("اضغط Enter للمتابعة...")
                
                elif choice == "3":
                    self.stop_monitoring()
                    input("اضغط Enter للمتابعة...")
                
                elif choice == "4":
                    self.show_report()
                    input("اضغط Enter للمتابعة...")
                
                elif choice == "5":
                    print_arabic("👋 goodbye!")
                    self.stop_monitoring()
                    break
                
                else:
                    print_arabic("❌ اختيار غير صحيح")
            
            except KeyboardInterrupt:
                print_arabic("\n\n⏹️ إيقاف النظام...")
                self.stop_monitoring()
                break

# تشغيل النظام
if __name__ == "__main__":
    # التحقق من وجود ملف الإعدادات
    if not os.path.exists('mobile_config.json'):
        print_arabic("⚠️ ملف الإعدادات غير موجود")
        print_arabic("سيتم استخدام الإعدادات الافتراضية")
    
    system = SimpleMobileParental()
    system.run_menu()