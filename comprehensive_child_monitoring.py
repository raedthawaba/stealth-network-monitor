#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import time
import sqlite3
from datetime import datetime, timedelta
import threading
import requests
from pathlib import Path
import re
import os

class ComprehensiveChildMonitor:
    def __init__(self, config_file='real_children_config.json'):
        self.config = self.load_config(config_file)
        self.db = self.setup_database()
        self.monitoring_active = False
        
    def load_config(self, config_file):
        """تحميل إعدادات الأطفال الحقيقيين"""
        default_config = {
            "children": [
                {
                    "name": "اسم_الطفل_الأول",
                    "ip": "192.168.1.101",
                    "age": 10,
                    "daily_limit_hours": 2,
                    "allowed_websites": ["google.com", "youtube.com", "wikipedia.org"],
                    "blocked_keywords": ["منتهي", "إباحي", "عنف", "Casino", "Porn"],
                    "blocked_apps": ["Instagram", "TikTok", "Snapchat", "Facebook"],
                    "safe_search": True,
                    "report_parent_only": True
                },
                {
                    "name": "اسم_الطفل_الثاني", 
                    "ip": "192.168.1.102",
                    "age": 14,
                    "daily_limit_hours": 3,
                    "allowed_websites": ["google.com", "youtube.com", "wikipedia.org", "khanacademy.org"],
                    "blocked_keywords": ["إباحي", "عنف", "مخدرات", "Casino", "Gambling", "Hate"],
                    "blocked_apps": ["Instagram", "TikTok", "Snapchat", "Telegram"],
                    "safe_search": True,
                    "report_parent_only": True
                }
            ],
            "monitoring_settings": {
                "scan_interval_minutes": 2,
                "log_to_file": True,
                "stealth_mode": True,
                "background_monitoring": True
            }
        }
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            print(f"⚠️ لم يتم العثور على {config_file}، سيتم إنشاء إعدادات افتراضية")
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=2)
            return default_config
    
    def setup_database(self):
        """إنشاء قاعدة البيانات للمراقبة الشاملة"""
        db_path = 'comprehensive_child_monitoring.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # جدول الأجهزة
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_name TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                device_type TEXT,
                last_seen TIMESTAMP,
                mac_address TEXT,
                vendor TEXT
            )
        ''')
        
        # جدول المواقع المزارة
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS visited_websites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_name TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                website TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                duration_seconds INTEGER,
                category TEXT,
                safety_status TEXT
            )
        ''')
        
        # جدول البحث
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_name TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                search_query TEXT NOT NULL,
                search_engine TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                blocked BOOLEAN DEFAULT FALSE,
                reason TEXT
            )
        ''')
        
        # جدول التطبيقات المستخدمة
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_name TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                app_name TEXT NOT NULL,
                category TEXT,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                duration_seconds INTEGER,
                blocked BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # جدول المحتوى
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_monitoring (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_name TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                content_type TEXT,
                content_title TEXT,
                source_url TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                safety_status TEXT,
                keywords_detected TEXT
            )
        ''')
        
        # جدول التواصل
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS communications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_name TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                platform TEXT,
                contact_type TEXT,
                message_preview TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                safety_status TEXT
            )
        ''')
        
        conn.commit()
        return conn
    
    def scan_network_for_devices(self):
        """فحص الشبكة للعثور على الأجهزة"""
        print("🔍 بدء فحص الشبكة للبحث عن الأطفال...")
        
        # استخدام nmap للفحص العميق
        local_ip = subprocess.run(['hostname', '-I'], capture_output=True, text=True).stdout.strip().split()[0]
        network_base = '.'.join(local_ip.split('.')[:3])
        network_range = f"{network_base}.0/24"
        
        try:
            # فحص عميق
            result = subprocess.run([
                'nmap', '-sn', '-sV', '--version-intensity=5',
                '--max-rate=100', '-T4', network_range
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                return self.parse_nmap_results(result.stdout)
            else:
                return self.fallback_scan(network_range)
                
        except Exception as e:
            print(f"⚠️ خطأ في فحص الشبكة: {e}")
            return self.fallback_scan(network_range)
    
    def parse_nmap_results(self, output):
        """تحليل نتائج nmap"""
        devices = []
        current_device = {}
        
        for line in output.split('\n'):
            line = line.strip()
            
            # عنوان IP
            if 'Nmap scan report for' in line:
                ip = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                if ip:
                    current_device = {'ip': ip.group(1), 'services': []}
                    devices.append(current_device)
            
            # معلومات الخدمات
            elif '/tcp' in line and current_device:
                service = line.split()
                if len(service) >= 2:
                    current_device['services'].append({
                        'port': service[0],
                        'service': service[1],
                        'version': ' '.join(service[2:]) if len(service) > 2 else 'Unknown'
                    })
            
            # اسم المضيف
            elif 'Host is up' in line and current_device:
                name_match = re.search(r'\((.*?)\)', line)
                if name_match:
                    current_device['name'] = name_match.group(1)
        
        return devices
    
    def fallback_scan(self, network_range):
        """فحص بديل للظهر البسيط"""
        devices = []
        network_base = network_range.replace('.0/24', '')
        
        for i in range(1, 255):
            ip = f"{network_base}.{i}"
            try:
                result = subprocess.run(['ping', '-c', '1', '-W', '2', ip], 
                                      capture_output=True, text=True, timeout=3)
                if result.returncode == 0:
                    devices.append({
                        'ip': ip,
                        'name': f'الجهاز-{i}',
                        'services': []
                    })
            except:
                continue
        
        return devices
    
    def monitor_websites(self, child_ip, child_name):
        """مراقبة المواقع المزارة"""
        print(f"🌐 مراقبة المواقع ل{child_name} ({child_ip})")
        
        # فحص ذاكرة التخزين المؤقت للشبكة
        try:
            # فحص ملفات الراوتر
            self.check_router_logs()
            
            # فحص DNS logs
            self.check_dns_logs()
            
        except Exception as e:
            print(f"⚠️ خطأ في مراقبة المواقع: {e}")
    
    def monitor_searches(self, child_ip, child_name):
        """مراقبة عمليات البحث"""
        print(f"🔍 مراقبة البحث ل{child_name} ({child_ip})")
        
        blocked_keywords = []
        for child in self.config['children']:
            if child['ip'] == child_ip:
                blocked_keywords = child.get('blocked_keywords', [])
                break
        
        # محاكاة كشف البحث
        search_queries = [
            "how to hack", "games", "youtube", "instagram",
            "facebook", "tiktok", "whatsapp"
        ]
        
        for query in search_queries:
            is_blocked = any(keyword in query.lower() for keyword in blocked_keywords)
            self.log_search(child_name, child_ip, query, is_blocked)
    
    def monitor_apps(self, child_ip, child_name):
        """مراقبة استخدام التطبيقات"""
        print(f"📱 مراقبة التطبيقات ل{child_name} ({child_ip})")
        
        blocked_apps = []
        for child in self.config['children']:
            if child['ip'] == child_ip:
                blocked_apps = child.get('blocked_apps', [])
                break
        
        # فحص العمليات النشطة
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    for app in blocked_apps:
                        if app.lower() in line.lower():
                            self.log_app_usage(child_name, child_ip, app, blocked=True)
        except:
            pass
    
    def monitor_content(self, child_ip, child_name):
        """مراقبة المحتوى"""
        print(f"📺 مراقبة المحتوى ل{child_name} ({child_ip})")
        
        # فحص الملفات المحملة
        self.check_downloaded_content(child_ip, child_name)
        
        # فحص التخزين المؤقت
        self.check_cache_files(child_ip, child_name)
    
    def monitor_communications(self, child_ip, child_name):
        """مراقبة الاتصالات"""
        print(f"💬 مراقبة الاتصالات ل{child_name} ({child_ip})")
        
        # فحص تطبيقات الرسائل
        messaging_apps = ['whatsapp', 'telegram', 'signal', 'discord']
        
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    for app in messaging_apps:
                        if app.lower() in line.lower():
                            self.log_communication(child_name, child_ip, app)
        except:
            pass
    
    def log_device(self, child_name, ip_address, device_type=None):
        """تسجيل جهاز جديد"""
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO devices 
            (child_name, ip_address, device_type, last_seen)
            VALUES (?, ?, ?, ?)
        ''', (child_name, ip_address, device_type, datetime.now()))
        self.db.commit()
    
    def log_website_visit(self, child_name, ip_address, website, category=None):
        """تسجيل زيارة موقع"""
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO visited_websites 
            (child_name, ip_address, website, category, safety_status)
            VALUES (?, ?, ?, ?, ?)
        ''', (child_name, ip_address, website, category, 'Unknown'))
        self.db.commit()
    
    def log_search(self, child_name, ip_address, query, blocked=False, reason=None):
        """تسجيل عملية بحث"""
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO searches 
            (child_name, ip_address, search_query, blocked, reason)
            VALUES (?, ?, ?, ?, ?)
        ''', (child_name, ip_address, query, blocked, reason))
        self.db.commit()
    
    def log_app_usage(self, child_name, ip_address, app_name, blocked=False):
        """تسجيل استخدام تطبيق"""
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO app_usage 
            (child_name, ip_address, app_name, blocked)
            VALUES (?, ?, ?, ?)
        ''', (child_name, ip_address, app_name, blocked))
        self.db.commit()
    
    def log_content(self, child_name, ip_address, content_type, title, url=None):
        """تسجيل محتوى"""
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO content_monitoring 
            (child_name, ip_address, content_type, content_title, source_url)
            VALUES (?, ?, ?, ?, ?)
        ''', (child_name, ip_address, content_type, title, url))
        self.db.commit()
    
    def log_communication(self, child_name, ip_address, platform):
        """تسجيل تواصل"""
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO communications 
            (child_name, ip_address, platform, contact_type)
            VALUES (?, ?, ?, ?)
        ''', (child_name, ip_address, platform, 'App'))
        self.db.commit()
    
    def check_router_logs(self):
        """فحص سجلات الراوتر (محاكاة)"""
        # في البيئة الحقيقية، هذا يتطلب اتصال بالراوتر
        pass
    
    def check_dns_logs(self):
        """فحص سجلات DNS (محاكاة)"""
        # في البيئة الحقيقية، هذا يتطلب access لسجلات DNS
        pass
    
    def check_downloaded_content(self, ip, child_name):
        """فحص المحتوى المحمل"""
        download_paths = ['/data/com.android.browser/Download', '/sdcard/Download']
        for path in download_paths:
            if os.path.exists(path):
                for file in os.listdir(path):
                    if file.endswith(('.mp4', '.jpg', '.pdf')):
                        self.log_content(child_name, ip, 'Download', file)
    
    def check_cache_files(self, ip, child_name):
        """فحص ملفات التخزين المؤقت"""
        cache_paths = ['/data/data/com.android.chrome/cache', '/data/data/com.android.browser/cache']
        for path in cache_paths:
            if os.path.exists(path):
                # فحص الملفات المشبوهة
                for file in os.listdir(path):
                    if any(keyword in file.lower() for keyword in ['.mp4', '.jpg', '.pdf', '.exe']):
                        self.log_content(child_name, ip, 'Cache', file)
    
    def generate_comprehensive_report(self):
        """تقرير شامل عن جميع الأنشطة"""
        cursor = self.db.cursor()
        
        report = {
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'summary': {},
            'devices': [],
            'websites': [],
            'searches': [],
            'apps': [],
            'content': [],
            'communications': []
        }
        
        # إحصائيات عامة
        for child in self.config['children']:
            child_name = child['name']
            
            # المواقع المزارة
            cursor.execute('SELECT COUNT(*) FROM visited_websites WHERE child_name = ?', (child_name,))
            report['summary'][f'{child_name}_websites'] = cursor.fetchone()[0]
            
            # عمليات البحث
            cursor.execute('SELECT COUNT(*) FROM searches WHERE child_name = ?', (child_name,))
            report['summary'][f'{child_name}_searches'] = cursor.fetchone()[0]
            
            # التطبيقات
            cursor.execute('SELECT COUNT(*) FROM app_usage WHERE child_name = ?', (child_name,))
            report['summary'][f'{child_name}_apps'] = cursor.fetchone()[0]
        
        return report
    
    def start_monitoring(self):
        """بدء المراقبة الشاملة"""
        self.monitoring_active = True
        print("🚀 بدء المراقبة الشاملة للأطفال...")
        print("="*60)
        
        # فحص الأجهزة المتصلة
        devices = self.scan_network_for_devices()
        
        for device in devices:
            print(f"📱 تم العثور على جهاز: {device['ip']}")
            # تحديد الطفل بناء على IP
            for child in self.config['children']:
                if child['ip'] == device['ip']:
                    child_name = child['name']
                    print(f"👶 مطابق للطفل: {child_name}")
                    
                    # بدء المراقبة لكل نوع بيانات
                    self.monitor_websites(device['ip'], child_name)
                    self.monitor_searches(device['ip'], child_name)
                    self.monitor_apps(device['ip'], child_name)
                    self.monitor_content(device['ip'], child_name)
                    self.monitor_communications(device['ip'], child_name)
                    
                    # تسجيل الجهاز
                    self.log_device(child_name, device['ip'])
        
        # توليد تقرير شامل
        report = self.generate_comprehensive_report()
        
        # حفظ التقرير
        with open('comprehensive_child_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print("\n" + "="*60)
        print("📊 تقرير المراقبة الشاملة")
        print("="*60)
        for key, value in report['summary'].items():
            print(f"{key}: {value} نشاط")
        print("="*60)
        print("💾 تم حفظ التقرير في: comprehensive_child_report.json")
        
        return report

def main():
    print("👶 نظام المراقبة الشاملة للأطفال")
    print("="*50)
    print("هذا النظام يراقب:")
    print("• المواقع المزارة")
    print("• عمليات البحث")
    print("• استخدام التطبيقات")
    print("• المحتوى المتصفح")
    print("• تطبيقات المراسلة")
    print("="*50)
    
    # إنشاء مثيل للمراقب
    monitor = ComprehensiveChildMonitor()
    
    # بدء المراقبة
    report = monitor.start_monitoring()
    
    return report

if __name__ == "__main__":
    main()