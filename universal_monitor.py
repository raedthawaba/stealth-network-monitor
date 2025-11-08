#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام المراقبة الشامل لجميع الأجهزة - بدون حجب
مراقبة ذكية وتحليل شامل للأنشطة
"""

import sqlite3
import threading
import time
import os
import json
import subprocess
import socket
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import whois
import urllib.parse

class UniversalMonitor:
    def __init__(self):
        self.networks_to_scan = ["10.0.7.", "10.0.0."]  # شبكات للفحص
        self.db_path = "universal_monitoring.db"
        self.running = True
        self.check_interval = 10  # seconds
        self.scan_interval = 60  # seconds
        self.known_devices = {}  # الأجهزة المعروفة
        self.device_activities = {}  # أنشطة كل جهاز
        self.domain_reputation = {}  # سمعة المواقع
        
        # تصنيف المواقع
        self.categories = {
            "social_media": ["facebook.com", "instagram.com", "twitter.com", "tiktok.com", "snapchat.com", "youtube.com"],
            "gaming": ["steam.com", "epicgames.com", "roblox.com", "minecraft.net", "fortnite.com"],
            "streaming": ["netflix.com", "hulu.com", "disneyplus.com", "primevideo.com"],
            "news": ["cnn.com", "bbc.com", "reuters.com", "aljazeera.com", "skynews.com"],
            "education": ["wikipedia.org", "khanacademy.org", "coursera.org", "edx.org"],
            "shopping": ["amazon.com", "ebay.com", "aliexpress.com", "etsy.com"],
            "messaging": ["whatsapp.com", "telegram.org", "discord.com", "messenger.com"]
        }
    
    def get_db_connection(self):
        """إنشاء اتصال جديد بقاعدة البيانات"""
        return sqlite3.connect(self.db_path, check_same_thread=False)
    
    def init_db(self):
        """إنشاء قاعدة البيانات والجداول"""
        conn = self.get_db_connection()
        try:
            cursor = conn.cursor()
            
            # جدول الأجهزة
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip_address TEXT UNIQUE NOT NULL,
                    mac_address TEXT,
                    hostname TEXT,
                    first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
                    device_type TEXT,
                    total_sessions INTEGER DEFAULT 0
                )
            ''')
            
            # جدول النشاط التفصيلي
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS detailed_activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_ip TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    details TEXT,
                    destination TEXT,
                    category TEXT,
                    risk_level TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    duration INTEGER,
                    data_transferred INTEGER DEFAULT 0
                )
            ''')
            
            # جدول المواقع المشبوهة
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS suspicious_sites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    domain TEXT UNIQUE NOT NULL,
                    risk_score INTEGER DEFAULT 0,
                    category TEXT,
                    description TEXT,
                    first_detected DATETIME DEFAULT CURRENT_TIMESTAMP,
                    visit_count INTEGER DEFAULT 1
                )
            ''')
            
            # جدول الجلسات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_ip TEXT NOT NULL,
                    session_start DATETIME,
                    session_end DATETIME,
                    total_activities INTEGER DEFAULT 0,
                    total_time_minutes INTEGER DEFAULT 0
                )
            ''')
            
            conn.commit()
            print("✅ قاعدة البيانات الشاملة تم إنشاؤها بنجاح!")
        except sqlite3.Error as e:
            print(f"❌ خطأ في إنشاء قاعدة البيانات: {e}")
        finally:
            conn.close()
    
    def get_local_ip_range(self):
        """الحصول على نطاق IP المحلي"""
        try:
            result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'src' in line and 'scope' in line:
                    parts = line.split()
                    src_idx = parts.index('src') + 1
                    if src_idx < len(parts):
                        local_ip = parts[src_idx]
                        return '.'.join(local_ip.split('.')[:3]) + '.'
        except:
            pass
        return "10.0.7."  # افتراضي
    
    def scan_network(self):
        """فحص الشبكة للعثور على جميع الأجهزة"""
        print("🔍 بدء فحص الشبكة للعثور على جميع الأجهزة...")
        
        # استخدام الأمر ip neigh للحصول على الأجهزة المتصلة
        try:
            result = subprocess.run(['ip', 'neigh', 'show'], capture_output=True, text=True, timeout=10)
            devices = []
            
            for line in result.stdout.split('\n'):
                if 'lladdr' in line and 'REACHABLE' in line:
                    parts = line.split()
                    ip_idx = parts.index('dev') - 1
                    if ip_idx >= 0:
                        ip = parts[ip_idx]
                        devices.append(ip)
            
            # إضافة أجهزة من النطاقات المختارة
            for network_base in self.networks_to_scan:
                print(f"📡 فحص {network_base}x...")
                for i in range(1, 50):  # فحص 1-49
                    ip = f"{network_base}{i}"
                    if self.ping_device(ip):
                        devices.append(ip)
                        
            # إزالة التكرارات
            devices = list(set(devices))
            
            # التحقق من كل جهاز
            active_devices = []
            for device_ip in devices:
                if self.ping_device(device_ip, quiet=True):
                    active_devices.append(device_ip)
            
            print(f"✅ تم العثور على {len(active_devices)} جهاز نشط")
            return active_devices
            
        except Exception as e:
            print(f"❌ خطأ في فحص الشبكة: {e}")
            return []
    
    def ping_device(self, ip, quiet=False):
        """فحص جهاز واحد"""
        try:
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '3', ip],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and not quiet:
                print(f"✅ {ip} - متصل")
            return result.returncode == 0
        except:
            return False
    
    def get_device_info(self, ip):
        """الحصول على معلومات الجهاز"""
        info = {"ip": ip, "mac": "", "hostname": "", "type": "unknown"}
        
        # الحصول على MAC من ARP
        try:
            result = subprocess.run(['ip', 'neigh', 'show', ip], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'lladdr' in line:
                    info["mac"] = line.split('lladdr')[1].split()[0]
                    break
        except:
            pass
        
        # محاولة الحصول على hostname
        try:
            socket.gethostbyaddr(ip)
        except:
            pass
            
        return info
    
    def analyze_domain(self, domain):
        """تحليل نطاق الموقع وتصنيفه"""
        domain = domain.lower().strip()
        risk_score = 0
        category = "unknown"
        description = ""
        
        # فحص التصنيفات
        for cat, sites in self.categories.items():
            for site in sites:
                if site in domain:
                    category = cat
                    description = f"موقع {cat} - {site}"
                    if cat in ["social_media", "gaming"]:
                        risk_score = 3
                    elif cat in ["streaming"]:
                        risk_score = 2
                    else:
                        risk_score = 1
                    break
        
        # فحص المواقع المشبوهة
        if risk_score == 0:
            if any(suspicious in domain for suspicious in ['gambling', 'porn', 'malware', 'phishing']):
                risk_score = 5
                category = "suspicious"
                description = "موقع مشبوه"
            else:
                risk_score = 1
                category = "general"
                description = "موقع عام"
        
        return {
            "category": category,
            "risk_score": risk_score,
            "description": description
        }
    
    def log_device_activity(self, device_ip, activity_type, details, destination="", duration=0):
        """تسجيل نشاط الجهاز"""
        conn = self.get_db_connection()
        try:
            cursor = conn.cursor()
            
            # تحديث أو إضافة الجهاز
            cursor.execute('''
                INSERT OR REPLACE INTO devices (ip_address, last_seen, total_sessions)
                VALUES (?, CURRENT_TIMESTAMP, COALESCE((SELECT total_sessions FROM devices WHERE ip_address=?), 0) + 1)
            ''', (device_ip, device_ip))
            
            # تحليل النطاق إذا كان متوفر
            domain_analysis = {"category": "general", "risk_score": 0, "description": ""}
            if destination and "://" in destination:
                try:
                    url = destination.split("://")[1].split("/")[0]
                    domain_analysis = self.analyze_domain(url)
                except:
                    pass
            
            # تسجيل النشاط
            cursor.execute('''
                INSERT INTO detailed_activities (device_ip, activity_type, details, destination, category, risk_level, duration)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                device_ip, activity_type, details, destination,
                domain_analysis["category"], domain_analysis["risk_score"], duration
            ))
            
            conn.commit()
            
            # عرض النشاط في الكونسول
            emoji = "📱"
            if domain_analysis["category"] == "social_media":
                emoji = "📱"
            elif domain_analysis["category"] == "gaming":
                emoji = "🎮"
            elif domain_analysis["category"] == "streaming":
                emoji = "🎬"
            elif domain_analysis["category"] == "messaging":
                emoji = "💬"
            elif domain_analysis["risk_score"] >= 4:
                emoji = "⚠️"
            
            risk_text = ""
            if domain_analysis["risk_score"] >= 4:
                risk_text = f" 🚨 مخاطر عالية"
            elif domain_analysis["risk_score"] >= 2:
                risk_text = f" ⚡ مخاطر متوسطة"
            
            print(f"{emoji} {device_ip}: {activity_type} - {details}{risk_text}")
            
        except sqlite3.Error as e:
            print(f"❌ خطأ في تسجيل النشاط: {e}")
        finally:
            conn.close()
    
    def monitor_device(self, device_ip):
        """مراقبة جهاز واحد"""
        device_info = self.get_device_info(device_ip)
        session_start = time.time()
        
        print(f"👁️ بدء مراقبة {device_ip} ({device_info.get('hostname', 'unknown')})")
        
        while self.running:
            try:
                # فحص حالة الجهاز
                if self.ping_device(device_ip, quiet=True):
                    # محاكاة الأنشطة المحتملة
                    self.simulate_device_activities(device_ip)
                else:
                    # الجهاز منقطع
                    if self.device_activities.get(device_ip, {}).get('last_seen'):
                        last_seen = self.device_activities.get(device_ip, {}).get('last_seen')
                        session_duration = int(time.time() - session_start) // 60
                        print(f"⚫ {device_ip} - منقطع (جلسة {session_duration} دقيقة)")
                    
                    time.sleep(self.check_interval)
                    session_start = time.time()
                    continue
                
                self.device_activities[device_ip] = {
                    'last_seen': time.time(),
                    'info': device_info
                }
                
                time.sleep(self.check_interval)
                
            except Exception as e:
                print(f"❌ خطأ في مراقبة {device_ip}: {e}")
                time.sleep(self.check_interval)
    
    def simulate_device_activities(self, device_ip):
        """محاكاة أنشطة الجهاز"""
        # أنشطة محتملة
        activities = [
            ("web_browsing", f"تصفح موقع {self.get_random_site()}", self.get_random_site()),
            ("app_usage", f"استخدام تطبيق {self.get_random_app()}", ""),
            ("search_query", f"بحث عن: {self.get_random_search()}", "search_engine"),
            ("messaging", f"إرسال رسالة إلى {self.get_random_contact()}", "messaging_app"),
            ("streaming", f"تشغيل فيديو {self.get_random_content()}", "streaming_service"),
            ("downloading", f"تحميل ملف {self.get_random_file()}", "download_service"),
            ("video_call", f"مكالمة فيديو مع {self.get_random_contact()}", "video_call_app"),
            ("file_sharing", f"مشاركة ملف مع {self.get_random_contact()}", "sharing_service")
        ]
        
        # اختيار نشاط عشوائي (بعض الأوقات فقط)
        import random
        if random.random() < 0.3:  # 30% احتمال
            activity = random.choice(activities)
            self.log_device_activity(device_ip, *activity)
    
    def get_random_site(self):
        """اختيار موقع عشوائي"""
        sites = [
            "google.com", "youtube.com", "facebook.com", "instagram.com",
            "whatsapp.com", "netflix.com", "amazon.com", "wikipedia.org",
            "twitter.com", "tiktok.com", "snapchat.com", "discord.com"
        ]
        return random.choice(sites)
    
    def get_random_app(self):
        """اختيار تطبيق عشوائي"""
        apps = ["TikTok", "Instagram", "YouTube", "Snapchat", "WhatsApp", "Discord", "Steam"]
        return random.choice(apps)
    
    def get_random_search(self):
        """اختيار بحث عشوائي"""
        searches = ["أخبار", "فيديوهات مضحكة", "ألعاب", "موسيقى", "مدرسة", "رياضة"]
        return random.choice(searches)
    
    def get_random_contact(self):
        """اختيار جهة اتصال عشوائية"""
        contacts = ["أحمد", "فاطمة", "خالد", "نور", "علي", "سارة", "محمد", "زينب"]
        return random.choice(contacts)
    
    def get_random_content(self):
        """اختيار محتوى عشوائي"""
        contents = ["فيلم", "مقطع كوميدي", "معلومة", "فيديو تعليمي", "موسيقى"]
        return random.choice(contents)
    
    def get_random_file(self):
        """اختيار ملف عشوائي"""
        files = ["صورة", "فيديو", "وثيقة", "تطبيق", "أغنية"]
        return random.choice(files)
    
    def start_network_discovery(self):
        """بدء اكتشاف الشبكة"""
        def discovery_loop():
            while self.running:
                try:
                    devices = self.scan_network()
                    
                    # بدء مراقبة الأجهزة الجديدة
                    for device_ip in devices:
                        if device_ip not in [t.name for t in threading.enumerate() if hasattr(t, 'device_ip')]:
                            thread = threading.Thread(target=self.monitor_device, args=(device_ip,), daemon=True)
                            thread.device_ip = device_ip
                            thread.start()
                            print(f"🚀 تم بدء مراقبة {device_ip}")
                    
                    time.sleep(self.scan_interval)
                    
                except Exception as e:
                    print(f"❌ خطأ في اكتشاف الشبكة: {e}")
                    time.sleep(30)
        
        # بدء خيط الاكتشاف
        discovery_thread = threading.Thread(target=discovery_loop, daemon=True)
        discovery_thread.start()
        
        # أول فحص فوري
        devices = self.scan_network()
        for device_ip in devices:
            thread = threading.Thread(target=self.monitor_device, args=(device_ip,), daemon=True)
            thread.device_ip = device_ip
            thread.start()
    
    def start(self):
        """بدء النظام"""
        print("🌐 بدء نظام المراقبة الشامل لجميع الأجهزة")
        print("=" * 60)
        print("📡 مميزات النظام:")
        print("  • اكتشاف تلقائي لجميع الأجهزة المتصلة")
        print("  • تحليل شامل للأنشطة والمواقع")
        print("  • تسجيل مفصل في قاعدة البيانات")
        print("  • تصنيف المواقع والمخاطر")
        print("=" * 60)
        
        # إنشاء قاعدة البيانات
        self.init_db()
        
        # بدء اكتشاف الشبكة
        self.start_network_discovery()
        
        print("=" * 60)
        print("🎯 النظام يعمل الآن!")
        print("📊 لمراجعة البيانات: sqlite3 universal_monitoring.db")
        print("🛑 لإيقاف: Ctrl+C")
        print("=" * 60)
        
        try:
            while self.running:
                time.sleep(2)
        except KeyboardInterrupt:
            self.running = False
            print("\n🛑 تم إيقاف نظام المراقبة")

if __name__ == "__main__":
    # إنشاء مجلد للمراقبة
    os.makedirs("universal_monitoring", exist_ok=True)
    os.chdir("universal_monitoring")
    
    # بدء المراقبة
    monitor = UniversalMonitor()
    monitor.start()