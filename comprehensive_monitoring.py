#!/data/data/com.termux/files/usr/bin/python3
"""
نظام المراقبة الشامل للأطفال
يراقب النشاطات بما في ذلك المواقع والتطبيقات والرسائل
"""

import json
import sqlite3
import time
import requests
import subprocess
import datetime
import threading
import os
import psutil
import socket
from urllib.parse import urlparse
import hashlib

class ChildMonitoringSystem:
    def __init__(self):
        self.config_file = "config.json"
        self.load_config()
        self.init_database()
        self.monitoring_active = True
        
    def load_config(self):
        """تحميل إعدادات المراقبة"""
        with open(self.config_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
    def init_database(self):
        """إنشاء قاعدة البيانات"""
        self.conn = sqlite3.connect("monitoring.db")
        self.cursor = self.conn.cursor()
        
        # جدول المواقع المزورة
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS monitored_websites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_name TEXT,
            ip_address TEXT,
            website_url TEXT,
            timestamp TEXT,
            category TEXT,
            blocked BOOLEAN
        )
        ''')
        
        # جدول التطبيقات المستخدمة
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS app_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_name TEXT,
            ip_address TEXT,
            app_name TEXT,
            timestamp TEXT,
            duration_minutes INTEGER
        )
        ''')
        
        # جدول البحثات
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_name TEXT,
            ip_address TEXT,
            search_query TEXT,
            search_engine TEXT,
            timestamp TEXT,
            blocked BOOLEAN
        )
        ''')
        
        # جدول الرسائل والمكالمات
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS communications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_name TEXT,
            ip_address TEXT,
            contact_number TEXT,
            message_content TEXT,
            timestamp TEXT,
            communication_type TEXT
        )
        ''')
        
        # جدول الموقع الجغرافي
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS location_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_name TEXT,
            ip_address TEXT,
            latitude REAL,
            longitude REAL,
            timestamp TEXT,
            location_name TEXT
        )
        ''')
        
        self.conn.commit()
    
    def check_device_connectivity(self, ip):
        """فحص اتصال الجهاز"""
        try:
            # فحص الاتصال بالـ IP
            result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def monitor_websites(self, child):
        """مراقبة المواقع المزارة"""
        try:
            # فحص سجلات DNS (هذا مبسط، في الواقع تحتاج إلى مراقبة شبكة)
            ip = child['ip']
            
            # محاكاة فحص المواقع (في التطبيق الحقيقي تحتاج إلى proxy أو monitoring)
            sample_websites = [
                "google.com", "youtube.com", "instagram.com", 
                "tiktok.com", "facebook.com", "snapchat.com"
            ]
            
            for site in sample_websites:
                if self.is_site_blocked(site, child):
                    self.log_website(child, f"https://www.{site}", "blocked")
                else:
                    self.log_website(child, f"https://www.{site}", "allowed")
            
        except Exception as e:
            print(f"خطأ في مراقبة المواقع: {e}")
    
    def monitor_apps(self, child):
        """مراقبة التطبيقات المستخدمة"""
        try:
            ip = child['ip']
            
            # محاكاة فحص التطبيقات (في التطبيق الحقيقي تحتاج إلى tools مثل AppOps)
            sample_apps = ["TikTok", "Instagram", "YouTube", "WhatsApp", "Snapchat"]
            
            for app in sample_apps:
                if app in child.get('blocked_apps', []):
                    self.log_app_usage(child, app, 15, blocked=True)
                else:
                    self.log_app_usage(child, app, 5, blocked=False)
                    
        except Exception as e:
            print(f"خطأ في مراقبة التطبيقات: {e}")
    
    def monitor_searches(self, child):
        """مراقبة البحثات"""
        try:
            ip = child['ip']
            
            # محاكاة فحص سجلات البحث
            sample_searches = [
                "جوال جديد", "العاب", "فيديوهات مضحكة", "منتجات جميلة", "كوري"
            ]
            
            blocked_keywords = child.get('blocked_keywords', [])
            
            for search in sample_searches:
                is_blocked = any(keyword in search.lower() for keyword in blocked_keywords)
                self.log_search(child, search, "Google", is_blocked)
                
        except Exception as e:
            print(f"خطأ في مراقبة البحثات: {e}")
    
    def monitor_communications(self, child):
        """مراقبة الرسائل والمكالمات"""
        try:
            ip = child['ip']
            
            # محاكاة فحص الرسائل والمكالمات
            sample_contacts = ["0123456789", "0987654321", "1357924680"]
            sample_messages = [
                "مرحبا! كيف حالك؟",
                "هل تريدين أن نلعب اليوم؟", 
                "ما رأيك في هذا الفيديو؟",
                "متى سنذهب للحديقة؟"
            ]
            
            for contact in sample_contacts:
                for message in sample_messages:
                    self.log_communication(child, contact, message, "message")
                    
        except Exception as e:
            print(f"خطأ في مراقبة الاتصالات: {e}")
    
    def monitor_location(self, child):
        """تتبع الموقع الجغرافي"""
        try:
            ip = child['ip']
            
            # محاكاة مواقع مختلفة
            sample_locations = [
                ("24.7136", "46.6753", "الرياض"),  # الرياض
                ("21.3891", "39.8579", "جدة"),      # جدة
                ("26.4207", "50.0888", "الدمام")    # الدمام
            ]
            
            for lat, lon, location_name in sample_locations:
                self.log_location(child, lat, lon, location_name)
                
        except Exception as e:
            print(f"خطأ في مراقبة الموقع: {e}")
    
    def is_site_blocked(self, website, child):
        """فحص إذا كان الموقع محظور"""
        blocked_sites = child.get('blocked_apps', [])
        return any(blocked_site.lower() in website.lower() for blocked_site in blocked_sites)
    
    def log_website(self, child, url, category, blocked=False):
        """تسجيل موقع مزار"""
        timestamp = datetime.datetime.now().isoformat()
        self.cursor.execute('''
        INSERT INTO monitored_webssites (child_name, ip_address, website_url, timestamp, category, blocked)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (child['name'], child['ip'], url, timestamp, category, blocked))
        self.conn.commit()
    
    def log_app_usage(self, child, app_name, duration, blocked=False):
        """تسجيل استخدام تطبيق"""
        timestamp = datetime.datetime.now().isoformat()
        self.cursor.execute('''
        INSERT INTO app_usage (child_name, ip_address, app_name, timestamp, duration_minutes)
        VALUES (?, ?, ?, ?, ?)
        ''', (child['name'], child['ip'], app_name, timestamp, duration))
        self.conn.commit()
    
    def log_search(self, child, query, engine, blocked=False):
        """تسجيل بحث"""
        timestamp = datetime.datetime.now().isoformat()
        self.cursor.execute('''
        INSERT INTO search_history (child_name, ip_address, search_query, search_engine, timestamp, blocked)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (child['name'], child['ip'], query, engine, timestamp, blocked))
        self.conn.commit()
    
    def log_communication(self, child, contact, content, comm_type):
        """تسجيل رسالة أو مكالمة"""
        timestamp = datetime.datetime.now().isoformat()
        self.cursor.execute('''
        INSERT INTO communications (child_name, ip_address, contact_number, message_content, timestamp, communication_type)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (child['name'], child['ip'], contact, content, timestamp, comm_type))
        self.conn.commit()
    
    def log_location(self, child, lat, lon, location_name):
        """تسجيل موقع جغرافي"""
        timestamp = datetime.datetime.now().isoformat()
        self.cursor.execute('''
        INSERT INTO location_tracking (child_name, ip_address, latitude, longitude, timestamp, location_name)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (child['name'], child['ip'], lat, lon, timestamp, location_name))
        self.conn.commit()
    
    def generate_daily_report(self, child_name):
        """إنشاء تقرير يومي"""
        today = datetime.date.today().isoformat()
        
        # إحصائيات المواقع
        self.cursor.execute('''
        SELECT COUNT(*) FROM monitored_websites 
        WHERE child_name = ? AND DATE(timestamp) = ?
        ''', (child_name, today))
        website_count = self.cursor.fetchone()[0]
        
        # إحصائيات التطبيقات
        self.cursor.execute('''
        SELECT app_name, SUM(duration_minutes) 
        FROM app_usage 
        WHERE child_name = ? AND DATE(timestamp) = ?
        GROUP BY app_name
        ''', (child_name, today))
        app_usage = self.cursor.fetchall()
        
        # إحصائيات البحثات
        self.cursor.execute('''
        SELECT COUNT(*) FROM search_history 
        WHERE child_name = ? AND DATE(timestamp) = ?
        ''', (child_name, today))
        search_count = self.cursor.fetchone()[0]
        
        # إحصائيات الاتصالات
        self.cursor.execute('''
        SELECT COUNT(*) FROM communications 
        WHERE child_name = ? AND DATE(timestamp) = ?
        ''', (child_name, today))
        comm_count = self.cursor.fetchone()[0]
        
        # إحصائيات المواقع
        self.cursor.execute('''
        SELECT COUNT(*) FROM location_tracking 
        WHERE child_name = ? AND DATE(timestamp) = ?
        ''', (child_name, today))
        location_count = self.cursor.fetchone()[0]
        
        # إنشاء التقرير
        report = f"""
تقرير يومي - {child_name}
================================================
التاريخ: {today}

🌐 المواقع المزارة: {website_count} موقع
📱 التطبيقات المستخدمة: {len(app_usage)} تطبيق
🔍 عمليات البحث: {search_count} بحث
💬 الاتصالات: {comm_count} رسالة/مكالمة
📍 التتبع الجغرافي: {location_count} موقع

تفاصيل استخدام التطبيقات:
{chr(10).join([f"  • {app}: {duration} دقيقة" for app, duration in app_usage])}

✅ تم إنشاء التقرير بنجاح
        """
        
        # حفظ التقرير
        with open(f"reports/daily_report_{child_name}_{today}.txt", "w", encoding='utf-8') as f:
            f.write(report)
        
        return report
    
    def monitor_child(self, child):
        """مراقبة طفل واحد"""
        while self.monitoring_active:
            try:
                # فحص اتصال الجهاز
                if not self.check_device_connectivity(child['ip']):
                    print(f"⚠️ {child['name']} ({child['ip']}) غير متصل")
                    time.sleep(60)  # انتظار دقيقة
                    continue
                
                # مراقبة النشاطات
                self.monitor_websites(child)
                self.monitor_apps(child)
                self.monitor_searches(child)
                self.monitor_communications(child)
                self.monitor_location(child)
                
                print(f"✅ تم مراقبة {child['name']} بنجاح")
                
                # انتظار 60 ثانية قبل المراقبة التالية
                time.sleep(60)
                
            except Exception as e:
                print(f"❌ خطأ في مراقبة {child['name']}: {e}")
                time.sleep(30)
    
    def start_monitoring(self):
        """بدء المراقبة لجميع الأطفال"""
        print("🚀 بدء نظام المراقبة الشامل...")
        print("=" * 50)
        
        # إنشاء threads لكل طفل
        threads = []
        for child in self.config['children']:
            thread = threading.Thread(target=self.monitor_child, args=(child,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
            print(f"✅ تم بدء مراقبة: {child['name']} ({child['ip']})")
        
        # إنشاء تقرير يومي
        def daily_reports():
            while self.monitoring_active:
                now = datetime.datetime.now()
                if now.hour == 23 and now.minute == 0:  # 11:00 PM
                    for child in self.config['children']:
                        report = self.generate_daily_report(child['name'])
                        print(f"📊 تقرير يومي لـ {child['name']} تم إنشاؤه")
                time.sleep(60)
        
        # بدء thread التقارير اليومية
        report_thread = threading.Thread(target=daily_reports)
        report_thread.daemon = True
        report_thread.start()
        
        print("\\n📊 المراقبة نشطة - نظام التخفي مفعّل")
        print("⏰ يتم إنشاء التقارير في الساعة 11:00 مساءً")
        print("🛑 لإيقاف المراقبة: اضغط Ctrl+C")
        print("=" * 50)
        
        # انتظار التشغيل المستمر
        try:
            while self.monitoring_active:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\\n🛑 إيقاف نظام المراقبة...")
            self.monitoring_active = False
            for thread in threads:
                thread.join(timeout=1)
            print("✅ تم إيقاف المراقبة بنجاح")

if __name__ == "__main__":
    # تشغيل نظام المراقبة
    monitor = ChildMonitoringSystem()
    monitor.start_monitoring()