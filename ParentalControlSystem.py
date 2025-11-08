#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام المراقبة الأبوية المتقدم للأطفال
لمراقبة وإدارة نشاط الأطفال على الشبكة بطريقة آمنة وتعليمية

الهدف: حماية الأطفال عبر الإنترنت مع احترام خصوصيتهم
"""

import os
import sys
import time
import json
import sqlite3
import socket
import threading
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import subprocess
import requests
from urllib.parse import urlparse
import hashlib

class ParentalDatabase:
    """قاعدة بيانات للمراقبة الأبوية"""
    
    def __init__(self, db_path: str = "parental_control.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """إنشاء قاعدة البيانات والجداول"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # جدول الأجهزة المتصلة
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT UNIQUE,
                hostname TEXT,
                mac_address TEXT,
                device_type TEXT,
                is_known_device BOOLEAN DEFAULT FALSE,
                child_name TEXT,
                age_range TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP
            )
        ''')
        
        # جدول النشاط على الإنترنت
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS internet_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_ip TEXT,
                url TEXT,
                domain TEXT,
                category TEXT,
                accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                duration_seconds INTEGER,
                is_blocked BOOLEAN DEFAULT FALSE,
                content_rating TEXT
            )
        ''')
        
        # جدول كلمات البحث
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_terms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_ip TEXT,
                search_term TEXT,
                search_engine TEXT,
                searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                result_count INTEGER,
                is_inappropriate BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # جدول التطبيقات المستخدمة
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_ip TEXT,
                app_name TEXT,
                app_category TEXT,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ended_at TIMESTAMP,
                duration_seconds INTEGER
            )
        ''')
        
        # جدول التنبيهات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_ip TEXT,
                alert_type TEXT,
                severity TEXT,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_read BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # جدول إعدادات التحكم
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

class NetworkMonitor:
    """مراقب الشبكة للكشف عن الأجهزة المتصلة"""
    
    def __init__(self, database: ParentalDatabase):
        self.database = database
        self.active_hosts = {}
        self.scan_interval = 30  # seconds
    
    def discover_devices(self, network_range: str = "192.168.1.0/24") -> List[Dict]:
        """اكتشاف جميع الأجهزة المتصلة بالشبكة"""
        devices = []
        
        try:
            # استخراج نطاق IP
            base_ip = network_range.split('/')[0]
            network_base = '.'.join(base_ip.split('.')[:3])
            
            for i in range(1, 255):
                ip = f"{network_base}.{i}"
                host_info = self.scan_host(ip)
                if host_info:
                    devices.append(host_info)
        
        except Exception as e:
            logging.error(f"خطأ في اكتشاف الأجهزة: {e}")
        
        return devices
    
    def scan_host(self, ip: str) -> Optional[Dict]:
        """فحص جهاز محدد على الشبكة"""
        try:
            # اختبار الاتصال
            response = subprocess.run(
                ['ping', '-n', '1', '-w', '1000', ip],
                capture_output=True, text=True, timeout=2
            )
            
            if response.returncode != 0:
                return None
            
            # الحصول على hostname
            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except:
                hostname = "غير معروف"
            
            # الحصول على معلومات إضافية
            mac_address = self.get_mac_address(ip)
            
            device_info = {
                'ip_address': ip,
                'hostname': hostname,
                'mac_address': mac_address,
                'last_seen': datetime.now(),
                'status': 'active'
            }
            
            # حفظ في قاعدة البيانات
            self.save_device_info(device_info)
            
            return device_info
            
        except Exception as e:
            logging.error(f"خطأ في فحص الجهاز {ip}: {e}")
            return None
    
    def get_mac_address(self, ip: str) -> str:
        """الحصول على عنوان MAC للجهاز"""
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(
                    ['arp', '-a', ip],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if ip in line:
                            parts = line.split()
                            if len(parts) >= 2:
                                return parts[1]
            else:  # Linux
                result = subprocess.run(
                    ['arp', '-n', ip],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if ip in line:
                            parts = line.split()
                            if len(parts) >= 3:
                                return parts[2]
        except:
            pass
        return "غير معروف"
    
    def save_device_info(self, device_info: Dict):
        """حفظ معلومات الجهاز في قاعدة البيانات"""
        conn = sqlite3.connect(self.database.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO devices 
            (ip_address, hostname, mac_address, last_seen)
            VALUES (?, ?, ?, ?)
        ''', (
            device_info['ip_address'],
            device_info['hostname'],
            device_info['mac_address'],
            device_info['last_seen']
        ))
        
        conn.commit()
        conn.close()

class WebActivityMonitor:
    """مراقب النشاط على الإنترنت"""
    
    def __init__(self, database: ParentalDatabase):
        self.database = database
        self.blocked_domains = set()
        self.inappropriate_keywords = set()
        self.safe_search_engines = {
            'google.com': 'نظام البحث الآمن',
            'bing.com': 'نظام البحث الآمن',
            'duckduckgo.com': 'البحث الآمن',
            'yahoo.com': 'البحث الآمن'
        }
        self.load_blocklists()
    
    def load_blocklists(self):
        """تحميل قوائم الحظر والكلمات غير المناسبة"""
        # قائمة المواقع الضارة والمخصصة
        harmful_domains = [
            'malware.com',
            'phishing.net',
            'adult-content.com'
        ]
        
        # كلمات البحث غير المناسبة للأطفال
        inappropriate_terms = [
            'adult', 'explicit', 'violence', 'gambling',
            'drugs', 'alcohol', 'tobacco', 'suicide'
        ]
        
        self.blocked_domains.update(harmful_domains)
        self.inappropriate_keywords.update(inappropriate_terms)
    
    def analyze_url(self, url: str, device_ip: str) -> Dict:
        """تحليل URL ومراجعته"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # فحص إذا كان الموقع محظور
            is_blocked = domain in self.blocked_domains
            
            # فحص محتوى الموقع
            category = self.categorize_website(domain)
            content_rating = self.get_content_rating(url)
            
            # تسجيل النشاط
            self.log_activity(device_ip, url, domain, category, is_blocked, content_rating)
            
            return {
                'url': url,
                'domain': domain,
                'is_blocked': is_blocked,
                'category': category,
                'content_rating': content_rating,
                'safe_for_children': not is_blocked and category in ['تعليمي', 'ترفيهي', 'ألعاب']
            }
        
        except Exception as e:
            logging.error(f"خطأ في تحليل URL: {e}")
            return {
                'url': url,
                'domain': 'غير معروف',
                'is_blocked': True,
                'category': 'خطأ',
                'content_rating': 'غير معروف',
                'safe_for_children': False
            }
    
    def categorize_website(self, domain: str) -> str:
        """تصنيف الموقع"""
        categories = {
            'تعليمي': ['wikipedia.org', 'khanacademy.org', 'education', 'learning'],
            'ترفيهي': ['youtube.com', 'netflix.com', 'disney.com', 'fun'],
            'ألعاب': ['poki.com', 'miniclip.com', 'roblox.com', 'games'],
            'أخبار': ['news', 'cnn.com', 'bbc.com', 'aljazeera.com'],
            'اجتماعي': ['facebook.com', 'instagram.com', 'twitter.com', 'snapchat.com'],
            'تسوق': ['amazon.com', 'ebay.com', 'aliexpress.com'],
            'غير مصنف': []
        }
        
        for category, keywords in categories.items():
            if any(keyword in domain for keyword in keywords):
                return category
        
        return 'غير مصنف'
    
    def get_content_rating(self, url: str) -> str:
        """تقييم محتوى الموقع للأطفال"""
        try:
            # فحص أساسي للمحتوى
            if 'adult' in url or 'explicit' in url:
                return 'غير مناسب'
            elif 'kids' in url or 'children' in url:
                return 'مناسب للأطفال'
            else:
                return 'يحتاج مراجعة'
        except:
            return 'غير معروف'
    
    def log_activity(self, device_ip: str, url: str, domain: str, 
                    category: str, is_blocked: bool, content_rating: str):
        """تسجيل نشاط الإنترنت"""
        conn = sqlite3.connect(self.database.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO internet_activity 
            (device_ip, url, domain, category, is_blocked, content_rating)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (device_ip, url, domain, category, is_blocked, content_rating))
        
        conn.commit()
        conn.close()
    
    def monitor_search_terms(self, search_term: str, search_engine: str, device_ip: str):
        """مراقبة كلمات البحث"""
        is_inappropriate = any(keyword in search_term.lower() for keyword in self.inappropriate_keywords)
        
        conn = sqlite3.connect(self.database.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO search_terms 
            (device_ip, search_term, search_engine, is_inappropriate)
            VALUES (?, ?, ?, ?)
        ''', (device_ip, search_term, search_engine, is_inappropriate))
        
        # إنشاء تنبيه إذا كان البحث غير مناسب
        if is_inappropriate:
            self.create_alert(device_ip, 'بحث غير مناسب', 'متوسط', f'الطفل بحث عن: {search_term}')
        
        conn.commit()
        conn.close()

class ApplicationMonitor:
    """مراقب التطبيقات المستخدمة"""
    
    def __init__(self, database: ParentalDatabase):
        self.database = database
        self.running_apps = {}
    
    def get_running_apps(self, device_ip: str) -> List[str]:
        """الحصول على التطبيقات المفتوحة حالياً"""
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(
                    ['tasklist', '/fo', 'csv'],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    lines = result.stdout.split('\n')[1:]  # تجاهل العنوان
                    apps = []
                    for line in lines:
                        if line.strip():
                            parts = line.split(',')
                            if len(parts) >= 1:
                                app_name = parts[0].strip('"')
                                apps.append(app_name)
                    return apps
            else:  # Linux
                result = subprocess.run(
                    ['ps', 'aux'],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    apps = []
                    for line in result.stdout.split('\n')[1:]:
                        if line.strip():
                            parts = line.split()
                            if len(parts) >= 11:
                                app_name = parts[10]
                                apps.append(app_name)
                    return apps
        except Exception as e:
            logging.error(f"خطأ في الحصول على التطبيقات: {e}")
        return []
    
    def categorize_app(self, app_name: str) -> str:
        """تصنيف التطبيق"""
        educational = ['chrome', 'firefox', 'word', 'excel', 'powerpoint', 'skype']
        gaming = ['steam', 'minecraft', 'fortnite', 'roblox', 'game']
        social = ['discord', 'whatsapp', 'facebook', 'instagram', 'telegram']
        streaming = ['netflix', 'youtube', 'spotify', 'hulu']
        productivity = ['notepad', 'calculator', 'paint', 'photoshop']
        
        app_lower = app_name.lower()
        
        if any(keyword in app_lower for keyword in educational):
            return 'تعليمي'
        elif any(keyword in app_lower for keyword in gaming):
            return 'ألعاب'
        elif any(keyword in app_lower for keyword in social):
            return 'اجتماعي'
        elif any(keyword in app_lower for keyword in streaming):
            return 'البث'
        elif any(keyword in app_lower for keyword in productivity):
            return 'إنتاجية'
        else:
            return 'أخرى'
    
    def log_app_usage(self, device_ip: str, app_name: str):
        """تسجيل استخدام التطبيق"""
        app_category = self.categorize_app(app_name)
        
        conn = sqlite3.connect(self.database.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO app_usage 
            (device_ip, app_name, app_category)
            VALUES (?, ?, ?)
        ''', (device_ip, app_name, app_category))
        
        conn.commit()
        conn.close()

class AlertSystem:
    """نظام التنبيهات للأمان"""
    
    def __init__(self, database: ParentalDatabase):
        self.database = database
        self.alert_thresholds = {
            'تطبيقات غير مناسبة': 3,
            'مواقع مشبوهة': 2,
            'وقت الشاشة المفرط': 4  # ساعات
        }
    
    def create_alert(self, device_ip: str, alert_type: str, severity: str, message: str):
        """إنشاء تنبيه أمني"""
        conn = sqlite3.connect(self.database.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alerts 
            (device_ip, alert_type, severity, message)
            VALUES (?, ?, ?, ?)
        ''', (device_ip, alert_type, severity, message))
        
        conn.commit()
        conn.close()
        
        # إرسال إشعار فوري للتنبيهات الخطيرة
        if severity == 'عالي':
            self.send_emergency_notification(device_ip, alert_type, message)
    
    def send_emergency_notification(self, device_ip: str, alert_type: str, message: str):
        """إرسال إشعار طوارئ للوالدين"""
        try:
            # يمكن تطوير هذا لإرسال إشعار عبر البريد الإلكتروني أو الهاتف
            notification = f"🚨 تنبيه أمني: {alert_type}\nالجهاز: {device_ip}\nالرسالة: {message}\nالوقت: {datetime.now()}"
            print(f"تنبيه طارئ: {notification}")
            
            # حفظ في ملف سجل
            with open('emergency_alerts.log', 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now()}: {notification}\n")
        
        except Exception as e:
            logging.error(f"خطأ في إرسال الإشعار: {e}")
    
    def check_for_alerts(self, device_ip: str):
        """فحص دوري للتنبيهات"""
        conn = sqlite3.connect(self.database.db_path)
        cursor = conn.cursor()
        
        # فحص التطبيقات غير المناسبة
        cursor.execute('''
            SELECT COUNT(*) FROM app_usage 
            WHERE device_ip = ? AND app_category = 'غير مصنف'
            AND started_at > datetime('now', '-1 hour')
        ''', (device_ip,))
        
        inappropriate_apps = cursor.fetchone()[0]
        if inappropriate_apps > self.alert_thresholds['تطبيقات غير مناسبة']:
            self.create_alert(device_ip, 'تطبيقات غير مناسبة', 'متوسط', 
                            f'تم اكتشاف {inappropriate_apps} تطبيق غير مصنف')
        
        # فحص المواقع المشبوهة
        cursor.execute('''
            SELECT COUNT(*) FROM internet_activity 
            WHERE device_ip = ? AND is_blocked = TRUE
            AND accessed_at > datetime('now', '-1 hour')
        ''', (device_ip,))
        
        blocked_sites = cursor.fetchone()[0]
        if blocked_sites > self.alert_thresholds['مواقع مشبوهة']:
            self.create_alert(device_ip, 'مواقع مشبوهة', 'عالي', 
                            f'تم محاولة访问 {blocked_sites} موقع محظور')
        
        conn.close()

class ReportGenerator:
    """مولد التقارير والأنشطة"""
    
    def __init__(self, database: ParentalDatabase):
        self.database = database
    
    def generate_daily_report(self, device_ip: str = None, child_name: str = None) -> Dict:
        """إنتاج تقرير يومي مفصل"""
        conn = sqlite3.connect(self.database.db_path)
        cursor = conn.cursor()
        
        # تحديد الجهاز المراد تتبعه
        device_filter = ""
        params = []
        if device_ip:
            device_filter = "WHERE device_ip = ?"
            params.append(device_ip)
        elif child_name:
            cursor.execute("SELECT ip_address FROM devices WHERE child_name = ?", (child_name,))
            result = cursor.fetchone()
            if result:
                device_filter = "WHERE device_ip = ?"
                params.append(result[0])
        
        # إحصائيات النشاط اليومي
        cursor.execute(f'''
            SELECT 
                COUNT(*) as total_sites,
                SUM(duration_seconds) as total_time,
                COUNT(CASE WHEN is_blocked = TRUE THEN 1 END) as blocked_sites,
                category,
                COUNT(*) as category_count
            FROM internet_activity 
            {device_filter} AND DATE(accessed_at) = DATE('now')
            GROUP BY category
        ''', params)
        
        categories = cursor.fetchall()
        
        # إحصائيات البحث
        cursor.execute(f'''
            SELECT 
                search_term,
                COUNT(*) as search_count
            FROM search_terms 
            {device_filter} AND DATE(searched_at) = DATE('now')
            GROUP BY search_term
            ORDER BY search_count DESC
            LIMIT 10
        ''', params)
        
        searches = cursor.fetchall()
        
        # إحصائيات التطبيقات
        cursor.execute(f'''
            SELECT 
                app_name,
                COUNT(*) as usage_count,
                SUM(duration_seconds) as total_time
            FROM app_usage 
            {device_filter} AND DATE(started_at) = DATE('now')
            GROUP BY app_name
            ORDER BY usage_count DESC
            LIMIT 10
        ''', params)
        
        apps = cursor.fetchall()
        
        # التنبيهات اليومية
        cursor.execute(f'''
            SELECT alert_type, severity, message, created_at
            FROM alerts 
            {device_filter} AND DATE(created_at) = DATE('now')
            ORDER BY created_at DESC
        ''', params)
        
        alerts = cursor.fetchall()
        
        conn.close()
        
        return {
            'report_date': datetime.now().strftime('%Y-%m-%d'),
            'device_ip': device_ip,
            'child_name': child_name,
            'website_categories': categories,
            'top_searches': searches,
            'top_apps': apps,
            'daily_alerts': alerts,
            'total_sites_visited': sum(row[0] for row in categories) if categories else 0,
            'blocked_attempts': sum(row[2] for row in categories) if categories else 0,
            'safety_score': self.calculate_safety_score(categories, searches, alerts)
        }
    
    def calculate_safety_score(self, categories: List, searches: List, alerts: List) -> int:
        """حساب نقاط الأمان (0-100)"""
        score = 100
        
        # خصم نقاط للكلمات البحث غير المناسبة
        inappropriate_searches = sum(1 for _, count in searches if count > 1)
        score -= inappropriate_searches * 5
        
        # خصم نقاط للتنبيهات
        high_severity_alerts = sum(1 for _, severity, _, _ in alerts if severity == 'عالي')
        medium_severity_alerts = sum(1 for _, severity, _, _ in alerts if severity == 'متوسط')
        
        score -= high_severity_alerts * 20
        score -= medium_severity_alerts * 10
        
        return max(0, min(100, score))
    
    def export_report_to_json(self, report: Dict, filename: str = None):
        """تصدير التقرير إلى ملف JSON"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"parental_report_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        
        return filename

class ParentalControlDashboard:
    """لوحة تحكم المراقبة الأبوية"""
    
    def __init__(self):
        self.database = ParentalDatabase()
        self.network_monitor = NetworkMonitor(self.database)
        self.web_monitor = WebActivityMonitor(self.database)
        self.app_monitor = ApplicationMonitor(self.database)
        self.alert_system = AlertSystem(self.database)
        self.report_generator = ReportGenerator(self.database)
        
        self.setup_logging()
    
    def setup_logging(self):
        """إعداد نظام السجلات"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('parental_control.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
    
    def add_child_device(self, ip_address: str, child_name: str, age_range: str, device_type: str = "كمبيوتر"):
        """إضافة جهاز طفل للمراقبة"""
        conn = sqlite3.connect(self.database.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO devices 
            (ip_address, child_name, age_range, device_type, is_known_device)
            VALUES (?, ?, ?, ?, ?)
        ''', (ip_address, child_name, age_range, device_type, True))
        
        conn.commit()
        conn.close()
        
        logging.info(f"تم إضافة جهاز الطفل: {child_name} ({ip_address})")
    
    def start_monitoring(self):
        """بدء المراقبة الشاملة"""
        print("🔍 بدء نظام المراقبة الأبوية المتقدم...")
        print("=" * 50)
        
        while True:
            try:
                # اكتشاف الأجهزة المتصلة
                print("🔎 فحص الأجهزة المتصلة...")
                devices = self.network_monitor.discover_devices()
                
                for device in devices:
                    ip = device['ip_address']
                    print(f"📱 تم اكتشاف جهاز: {ip} - {device['hostname']}")
                    
                    # فحص التطبيقات المفتوحة
                    running_apps = self.app_monitor.get_running_apps(ip)
                    for app in running_apps:
                        self.app_monitor.log_app_usage(ip, app)
                    
                    # فحص التنبيهات
                    self.alert_system.check_for_alerts(ip)
                
                # انتظار للفحص التالي
                time.sleep(self.network_monitor.scan_interval)
                
            except KeyboardInterrupt:
                print("\n🛑 تم إيقاف المراقبة بواسطة المستخدم")
                break
            except Exception as e:
                logging.error(f"خطأ في المراقبة: {e}")
                time.sleep(5)
    
    def show_dashboard(self):
        """عرض لوحة التحكم"""
        print("\n" + "="*60)
        print("🏠 لوحة تحكم المراقبة الأبوية")
        print("="*60)
        
        conn = sqlite3.connect(self.database.db_path)
        cursor = conn.cursor()
        
        # الأجهزة المتصلة
        cursor.execute("SELECT * FROM devices WHERE is_known_device = TRUE")
        children = cursor.fetchall()
        
        print(f"\n👶 الأطفال المراقبون ({len(children)}):")
        for child in children:
            print(f"  • {child[6]} ({child[2]}) - {child[7]}")
        
        # التنبيهات الحديثة
        cursor.execute('''
            SELECT * FROM alerts 
            WHERE is_read = FALSE 
            ORDER BY created_at DESC 
            LIMIT 5
        ''')
        alerts = cursor.fetchall()
        
        print(f"\n🚨 تنبيهات حديثة ({len(alerts)}):")
        for alert in alerts:
            print(f"  • {alert[2]}: {alert[4]} ({alert[3]})")
        
        # إحصائيات اليوم
        cursor.execute('''
            SELECT 
                COUNT(*) as sites_visited,
                COUNT(CASE WHEN is_blocked = TRUE THEN 1 END) as blocked_sites
            FROM internet_activity 
            WHERE DATE(accessed_at) = DATE('now')
        ''')
        stats = cursor.fetchone()
        
        print(f"\n📊 إحصائيات اليوم:")
        print(f"  • المواقع المزارة: {stats[0]}")
        print(f"  • المواقع المحظورة: {stats[1]}")
        
        conn.close()
    
    def get_recommendations(self) -> List[str]:
        """الحصول على توصيات للوالدين"""
        recommendations = []
        
        conn = sqlite3.connect(self.database.db_path)
        cursor = conn.cursor()
        
        # فحص استخدام الشاشة
        cursor.execute('''
            SELECT SUM(duration_seconds)/3600 as total_hours
            FROM internet_activity 
            WHERE DATE(accessed_at) = DATE('now')
        ''')
        hours = cursor.fetchone()[0] or 0
        
        if hours > 4:
            recommendations.append("⚠️ وقت الشاشة اليومي مفرط، ينصح بتقليله")
        
        # فحص البحث غير المناسب
        cursor.execute('''
            SELECT COUNT(*) FROM search_terms 
            WHERE DATE(searched_at) = DATE('now') AND is_inappropriate = TRUE
        ''')
        inappropriate_searches = cursor.fetchone()[0]
        
        if inappropriate_searches > 0:
            recommendations.append(f"🔍 تم رصد {inappropriate_searches} بحث غير مناسب اليوم")
        
        # فحص المواقع الاجتماعية
        cursor.execute('''
            SELECT COUNT(*) FROM internet_activity 
            WHERE DATE(accessed_at) = DATE('now') AND category = 'اجتماعي'
        ''')
        social_time = cursor.fetchone()[0]
        
        if social_time > 10:
            recommendations.append("💬 الوقت على مواقع التواصل الاجتماعي مرتفع")
        
        conn.close()
        
        if not recommendations:
            recommendations.append("✅ النشاط آمن ومقبول اليوم")
        
        return recommendations

def main():
    """الدالة الرئيسية"""
    print("🛡️ نظام المراقبة الأبوية المتقدم للأطفال")
    print("=" * 50)
    print("تهدف هذه الأداة لحماية الأطفال عبر الإنترنت")
    print("مع احترام خصوصيتهم وتوجيههم بطريقة تعليمية")
    print("=" * 50)
    
    dashboard = ParentalControlDashboard()
    
    # إضافة الأطفال المراد مراقبتهم
    while True:
        print("\nهل تريد إضافة طفل للمراقبة؟ (y/n)")
        choice = input("اختيارك: ").lower().strip()
        
        if choice == 'n':
            break
        
        child_name = input("اسم الطفل: ").strip()
        age_range = input("الفئة العمرية (مثال: 8-12): ").strip()
        device_ip = input("عنوان IP للجهاز: ").strip()
        device_type = input("نوع الجهاز (كمبيوتر/هاتف/جهاز لوحي): ").strip() or "كمبيوتر"
        
        dashboard.add_child_device(device_ip, child_name, age_range, device_type)
        print(f"✅ تم إضافة {child_name} للمراقبة")
    
    # عرض لوحة التحكم
    dashboard.show_dashboard()
    
    # عرض التوصيات
    print("\n💡 توصيات اليوم:")
    recommendations = dashboard.get_recommendations()
    for rec in recommendations:
        print(f"  {rec}")
    
    # بدء المراقبة
    print("\nهل تريد بدء المراقبة الفورية؟ (y/n)")
    start_choice = input("اختيارك: ").lower().strip()
    
    if start_choice == 'y':
        print("\n⚠️ تأكد من:")
        print("1. الحصول على موافقة الأطفال على المراقبة")
        print("2. استخدام هذه الأداة للأمان وليس التجسس")
        print("3. التحدث مع الأطفال حول السلامة الرقمية")
        print("\nبدء المراقبة...")
        dashboard.start_monitoring()
    else:
        print("تم إنشاء النظام. يمكنك تشغيله لاحقاً.")

if __name__ == "__main__":
    main()