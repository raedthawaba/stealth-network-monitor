#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام المراقبة الأبوية المتقدم - الإصدار المحسن
يوفر مراقبة دقيقة للتطبيقات، البحث، المشاهدة، وأجهزة الشبكة
"""

import os
import sys
import json
import sqlite3
import time
import socket
import threading
import psutil
import subprocess
import requests
import platform
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set
import winreg  # For Windows (will be imported conditionally)
import wmi  # For Windows process monitoring
import ifcfg  # For network interface detection

class AdvancedParentalMonitor:
    """نظام المراقبة الأبوية المتقدم"""
    
    def __init__(self, config_path: str = "parental_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.db_path = "advanced_parental_control.db"
        self.init_database()
        self.monitoring_active = False
        self.child_devices = {}
        
    def load_config(self) -> Dict:
        """تحميل إعدادات النظام"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ خطأ في تحميل الإعدادات: {e}")
            return {}
    
    def init_database(self):
        """إنشاء قاعدة البيانات المحسنة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # جدول الأجهزة المحسن
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
                os_type TEXT,
                last_seen TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول التطبيقات المفتوحة
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS open_applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_ip TEXT,
                process_name TEXT,
                process_id INTEGER,
                window_title TEXT,
                start_time TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                child_name TEXT,
                FOREIGN KEY (device_ip) REFERENCES devices (ip_address)
            )
        ''')
        
        # جدول البحث المتقدم
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_ip TEXT,
                search_engine TEXT,
                search_terms TEXT,
                search_url TEXT,
                results_count INTEGER,
                clicked_links TEXT,
                search_time TIMESTAMP,
                is_inappropriate BOOLEAN DEFAULT FALSE,
                child_name TEXT,
                risk_level TEXT,
                FOREIGN KEY (device_ip) REFERENCES devices (ip_address)
            )
        ''')
        
        # جدول المشاهدة والمحتوى
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS viewing_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_ip TEXT,
                content_type TEXT,
                content_title TEXT,
                content_url TEXT,
                duration_minutes INTEGER,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                category TEXT,
                is_blocked BOOLEAN DEFAULT FALSE,
                child_name TEXT,
                safety_score REAL,
                FOREIGN KEY (device_ip) REFERENCES devices (ip_address)
            )
        ''')
        
        # جدول موقع الشبكة المتقدم
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS network_connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_ip TEXT,
                remote_ip TEXT,
                remote_port INTEGER,
                protocol TEXT,
                connection_state TEXT,
                data_sent INTEGER,
                data_received INTEGER,
                connection_start TIMESTAMP,
                connection_end TIMESTAMP,
                child_name TEXT,
                FOREIGN KEY (device_ip) REFERENCES devices (ip_address)
            )
        ''')
        
        # جدول التحليلات والتنبيهات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_ip TEXT,
                alert_type TEXT,
                alert_level TEXT,
                description TEXT,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_resolved BOOLEAN DEFAULT FALSE,
                child_name TEXT,
                FOREIGN KEY (device_ip) REFERENCES devices (ip_address)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ تم إنشاء قاعدة البيانات المحسنة")
    
    def scan_network_devices(self) -> List[Dict]:
        """فحص أجهزة الشبكة المتقدمة"""
        devices = []
        try:
            import ipaddress
            network = ipaddress.IPv4Network(self.config.get('system_settings', {}).get('network_range', '192.168.1.0/24'), strict=False)
            
            for ip in network.hosts():
                if self.is_device_reachable(str(ip)):
                    device_info = self.get_device_details(str(ip))
                    if device_info:
                        devices.append(device_info)
        except Exception as e:
            print(f"⚠️ خطأ في فحص الشبكة: {e}")
        
        return devices
    
    def is_device_reachable(self, ip: str) -> bool:
        """فحص إذا كان الجهاز قابل للوصول"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(['ping', '-n', '1', '-w', '1000', ip], 
                                      capture_output=True, text=True, timeout=2)
            else:
                result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                                      capture_output=True, text=True, timeout=2)
            return result.returncode == 0
        except:
            return False
    
    def get_device_details(self, ip: str) -> Optional[Dict]:
        """الحصول على تفاصيل الجهاز"""
        try:
            hostname = self.get_hostname(ip)
            mac = self.get_mac_address(ip)
            device_type = self.guess_device_type(hostname, ip)
            os_type = self.detect_os(ip)
            
            return {
                'ip_address': ip,
                'hostname': hostname or 'Unknown',
                'mac_address': mac or 'Unknown',
                'device_type': device_type,
                'os_type': os_type,
                'is_known': self.is_known_device(ip),
                'child_name': self.get_child_name_by_ip(ip)
            }
        except Exception as e:
            print(f"⚠️ خطأ في الحصول على تفاصيل {ip}: {e}")
            return None
    
    def get_hostname(self, ip: str) -> Optional[str]:
        """الحصول على اسم المضيف"""
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return None
    
    def get_mac_address(self, ip: str) -> Optional[str]:
        """الحصول على عنوان MAC"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(['arp', '-a', ip], capture_output=True, text=True)
                lines = result.stdout.split('\n')
                for line in lines:
                    if ip in line:
                        parts = line.split()
                        if len(parts) >= 2:
                            return parts[1].replace('-', ':').lower()
            else:
                result = subprocess.run(['arp', '-n', ip], capture_output=True, text=True)
                lines = result.stdout.split('\n')
                for line in lines:
                    if ip in line:
                        parts = line.split()
                        if len(parts) >= 3:
                            return parts[2].lower()
        except:
            pass
        return None
    
    def guess_device_type(self, hostname: str, ip: str) -> str:
        """تخمين نوع الجهاز"""
        if not hostname:
            return "Unknown"
        
        hostname_lower = hostname.lower()
        if any(x in hostname_lower for x in ['phone', 'mobile', 'android', 'iphone']):
            return "هاتف ذكي"
        elif any(x in hostname_lower for x in ['tablet', 'ipad']):
            return "جهاز لوحي"
        elif any(x in hostname_lower for x in ['laptop', 'computer', 'pc', 'desktop']):
            return "كمبيوتر"
        else:
            return "جهاز غير محدد"
    
    def detect_os(self, ip: str) -> str:
        """كشف نوع نظام التشغيل"""
        try:
            if platform.system() == "Windows":
                # محاولة استخدام WMI لكشف Windows
                c = wmi.WMI()
                for os in c.Win32_OperatingSystem():
                    return "Windows"
            else:
                # محاولة ping مع TTL لفهم نوع النظام
                if platform.system() == "Linux":
                    return "Linux"
                elif platform.system() == "Darwin":
                    return "macOS"
        except:
            pass
        return "Unknown"
    
    def is_known_device(self, ip: str) -> bool:
        """فحص إذا كان الجهاز معروفاً"""
        for child in self.config.get('children', []):
            if child.get('device_ip') == ip and child.get('is_active', False):
                return True
        return False
    
    def get_child_name_by_ip(self, ip: str) -> Optional[str]:
        """الحصول على اسم الطفل بواسطة IP"""
        for child in self.config.get('children', []):
            if child.get('device_ip') == ip:
                return child.get('name')
        return None
    
    def monitor_processes(self, child_ip: str) -> List[Dict]:
        """مراقبة العمليات والتطبيقات المفتوحة"""
        processes = []
        try:
            child_name = self.get_child_name_by_ip(child_ip)
            if not child_name:
                return processes
            
            # مراقبة العمليات على النظام المحلي (يجب تطويرها للجهاز البعيد)
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
                try:
                    proc_info = {
                        'process_name': proc.info['name'],
                        'process_id': proc.info['pid'],
                        'command_line': ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else '',
                        'start_time': datetime.fromtimestamp(proc.info['create_time']),
                        'window_title': self.get_window_title(proc.info['pid']),
                        'child_name': child_name,
                        'is_suspicious': self.is_suspicious_process(proc.info['name'])
                    }
                    processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            print(f"⚠️ خطأ في مراقبة العمليات: {e}")
        
        return processes
    
    def get_window_title(self, pid: int) -> str:
        """الحصول على عنوان النافذة"""
        try:
            if platform.system() == "Windows":
                import win32gui
                def enum_windows_callback(hwnd, windows):
                    if win32gui.IsWindowVisible(hwnd):
                        window_text = win32gui.GetWindowText(hwnd)
                        _, found_pid = win32gui.GetWindowThreadProcessId(hwnd)
                        if found_pid == pid and window_text:
                            windows.append(window_text)
                    return True
                
                windows = []
                win32gui.EnumWindows(enum_windows_callback, windows)
                return windows[0] if windows else ""
        except:
            pass
        return ""
    
    def is_suspicious_process(self, process_name: str) -> bool:
        """فحص إذا كانت العملية مشبوهة"""
        suspicious_keywords = [
            'hack', 'crack', 'keylogger', 'malware', 'virus',
            'torrent', 'peer', 'download', 'p2p', 'proxy',
            'vpn', 'tor', 'anonymous', 'exploit'
        ]
        
        process_lower = process_name.lower()
        return any(keyword in process_lower for keyword in suspicious_keywords)
    
    def monitor_search_activities(self, device_ip: str) -> List[Dict]:
        """مراقبة أنشطة البحث"""
        searches = []
        try:
            # مراقبة ملفات السجل (يجب تطويرها)
            # هذه مثال للبحث في ملفات السجل
            browser_logs = self.get_browser_search_logs(device_ip)
            for log in browser_logs:
                search_info = {
                    'search_engine': log.get('engine', 'Unknown'),
                    'search_terms': log.get('terms', ''),
                    'search_url': log.get('url', ''),
                    'search_time': log.get('timestamp', datetime.now()),
                    'is_inappropriate': self.is_inappropriate_search(log.get('terms', '')),
                    'risk_level': self.calculate_search_risk(log.get('terms', '')),
                    'child_name': self.get_child_name_by_ip(device_ip)
                }
                searches.append(search_info)
                
        except Exception as e:
            print(f"⚠️ خطأ في مراقبة البحث: {e}")
        
        return searches
    
    def get_browser_search_logs(self, device_ip: str) -> List[Dict]:
        """الحصول على سجلات البحث من المتصفح"""
        # هذه مثال - يجب تطويرها حسب المتصفح ونظام التشغيل
        return [
            {
                'engine': 'google.com',
                'terms': 'math homework help',
                'url': 'https://www.google.com/search?q=math+homework+help',
                'timestamp': datetime.now()
            }
        ]
    
    def is_inappropriate_search(self, search_terms: str) -> bool:
        """فحص إذا كان البحث غير مناسب"""
        inappropriate_keywords = [
            'adult', 'explicit', 'violence', 'gambling', 'drugs',
            'alcohol', 'tobacco', 'suicide', 'hate speech', 'cyberbullying',
            'porn', 'nude', 'sex', 'weapon', 'bomb', 'terrorist'
        ]
        
        search_lower = search_terms.lower()
        return any(keyword in search_lower for keyword in inappropriate_keywords)
    
    def calculate_search_risk(self, search_terms: str) -> str:
        """حساب مستوى خطر البحث"""
        inappropriate_keywords = [
            'adult', 'explicit', 'violence', 'gambling', 'drugs',
            'alcohol', 'tobacco', 'suicide', 'hate speech', 'cyberbullying',
            'porn', 'nude', 'sex', 'weapon', 'bomb', 'terrorist'
        ]
        
        search_lower = search_terms.lower()
        matches = sum(1 for keyword in inappropriate_keywords if keyword in search_lower)
        
        if matches >= 3:
            return "عالي"
        elif matches >= 1:
            return "متوسط"
        else:
            return "منخفض"
    
    def monitor_viewing_activities(self, device_ip: str) -> List[Dict]:
        """مراقبة أنشطة المشاهدة"""
        viewing_activities = []
        try:
            # مراقبة الفيديوهات والمواقع المزارة
            browser_history = self.get_browser_history(device_ip)
            for item in browser_history:
                activity = {
                    'content_type': self.determine_content_type(item.get('url', '')),
                    'content_title': item.get('title', 'Unknown'),
                    'content_url': item.get('url', ''),
                    'start_time': item.get('timestamp', datetime.now()),
                    'category': self.categorize_content(item.get('url', '')),
                    'is_blocked': self.is_blocked_content(item.get('url', '')),
                    'safety_score': self.calculate_safety_score(item.get('url', '')),
                    'child_name': self.get_child_name_by_ip(device_ip)
                }
                viewing_activities.append(activity)
                
        except Exception as e:
            print(f"⚠️ خطأ في مراقبة المشاهدة: {e}")
        
        return viewing_activities
    
    def get_browser_history(self, device_ip: str) -> List[Dict]:
        """الحصول على تاريخ المتصفح"""
        # مثال - يجب تطويرها حسب المتصفح
        return [
            {
                'title': 'كيفية حل المعادلات الرياضية',
                'url': 'https://khanacademy.org/math/algebra',
                'timestamp': datetime.now()
            }
        ]
    
    def determine_content_type(self, url: str) -> str:
        """تحديد نوع المحتوى"""
        if any(ext in url.lower() for ext in ['.mp4', '.avi', '.mkv', '.mov']):
            return "فيديو"
        elif any(ext in url.lower() for ext in ['.mp3', '.wav', '.flac']):
            return "صوت"
        elif any(ext in url.lower() for ext in ['.pdf', '.doc', '.docx']):
            return "مستند"
        elif any(domain in url.lower() for domain in ['youtube.com', 'vimeo.com']):
            return "فيديو"
        elif any(domain in url.lower() for domain in ['netflix.com', 'hulu.com']):
            return "فيديو"
        elif 'google.com/search' in url:
            return "بحث"
        else:
            return "موقع ويب"
    
    def categorize_content(self, url: str) -> str:
        """تصنيف المحتوى"""
        educational_sites = [
            'khanacademy.org', 'wikipedia.org', 'scholastic.com',
            'coursera.org', 'edx.org', 'mit.edu', 'stanford.edu'
        ]
        
        entertainment_sites = [
            'youtube.com', 'netflix.com', 'hulu.com', 'disney.com',
            'nickelodeon.com', 'cartoon-network.com'
        ]
        
        social_sites = [
            'facebook.com', 'twitter.com', 'instagram.com', 'snapchat.com',
            'tiktok.com', 'whatsapp.com', 'telegram.org'
        ]
        
        gaming_sites = [
            'steampowered.com', 'epicgames.com', 'minecraft.net',
            'roblox.com', 'fortnite.com'
        ]
        
        url_lower = url.lower()
        
        if any(site in url_lower for site in educational_sites):
            return "تعليمي"
        elif any(site in url_lower for site in entertainment_sites):
            return "ترفيهي"
        elif any(site in url_lower for site in social_sites):
            return "اجتماعي"
        elif any(site in url_lower for site in gaming_sites):
            return "ألعاب"
        else:
            return "عام"
    
    def is_blocked_content(self, url: str) -> bool:
        """فحص إذا كان المحتوى محظوراً"""
        blocked_domains = [
            'porn', 'adult', 'explicit', 'xvideos', 'pornhub',
            'gambling', 'casino', 'bet', 'poker'
        ]
        
        blocked_keywords = [
            'violence', 'weapon', 'bomb', 'terrorist', 'drugs',
            'alcohol', 'nude', 'sex', 'suicide'
        ]
        
        url_lower = url.lower()
        
        return (any(domain in url_lower for domain in blocked_domains) or
                any(keyword in url_lower for keyword in blocked_keywords))
    
    def calculate_safety_score(self, url: str) -> float:
        """حساب نقاط الأمان للمحتوى"""
        score = 1.0
        
        # إضافة نقاط لل المواقع التعليمية
        educational_sites = [
            'khanacademy.org', 'wikipedia.org', 'scholastic.com',
            'coursera.org', 'edx.org'
        ]
        
        if any(site in url.lower() for site in educational_sites):
            score += 0.3
        
        # خصم نقاط للمواقع المحظورة
        if self.is_blocked_content(url):
            score -= 0.5
        
        # المواقع المشبوهة
        suspicious_domains = [
            'bit.ly', 'tinyurl.com', 'adf.ly', 'shorte.st'
        ]
        
        if any(domain in url.lower() for domain in suspicious_domains):
            score -= 0.2
        
        return max(0.0, min(1.0, score))
    
    def generate_comprehensive_report(self) -> Dict:
        """إنشاء تقرير شامل"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'devices_monitored': [],
            'total_activities': {},
            'risk_analysis': {},
            'recommendations': []
        }
        
        try:
            # تقرير الأجهزة المراقبة
            cursor.execute('''
                SELECT ip_address, child_name, device_type, is_known_device
                FROM devices WHERE is_known_device = 1
            ''')
            devices = cursor.fetchall()
            
            for device in devices:
                device_info = {
                    'ip_address': device[0],
                    'child_name': device[1],
                    'device_type': device[2],
                    'is_known': bool(device[3])
                }
                
                # عدد التطبيقات المفتوحة
                cursor.execute('''
                    SELECT COUNT(*) FROM open_applications 
                    WHERE device_ip = ? AND is_active = 1
                ''', (device[0],))
                app_count = cursor.fetchone()[0]
                device_info['active_applications'] = app_count
                
                # عدد عمليات البحث
                cursor.execute('''
                    SELECT COUNT(*) FROM search_activities 
                    WHERE device_ip = ? AND DATE(search_time) = DATE('now')
                ''', (device[0],))
                search_count = cursor.fetchone()[0]
                device_info['today_searches'] = search_count
                
                # عدد المواقع المزارة
                cursor.execute('''
                    SELECT COUNT(*) FROM viewing_activities 
                    WHERE device_ip = ? AND DATE(start_time) = DATE('now')
                ''', (device[0],))
                view_count = cursor.fetchone()[0]
                device_info['today_visits'] = view_count
                
                # مستوى الخطر
                cursor.execute('''
                    SELECT COUNT(*) FROM analysis_alerts 
                    WHERE device_ip = ? AND DATE(created_at) = DATE('now') 
                    AND alert_level = 'عالي'
                ''', (device[0],))
                high_risk_count = cursor.fetchone()[0]
                device_info['high_risk_alerts'] = high_risk_count
                
                report['devices_monitored'].append(device_info)
            
            # إحصائيات عامة
            cursor.execute('SELECT COUNT(*) FROM devices')
            report['total_activities']['total_devices'] = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM open_applications')
            report['total_activities']['total_applications'] = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM search_activities')
            report['total_activities']['total_searches'] = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM viewing_activities')
            report['total_activities']['total_visits'] = cursor.fetchone()[0]
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء التقرير: {e}")
        finally:
            conn.close()
        
        return report
    
    def start_monitoring(self):
        """بدء المراقبة المتقدمة"""
        self.monitoring_active = True
        print("🚀 بدء المراقبة المتقدمة...")
        
        # فحص الأجهزة أولاً
        devices = self.scan_network_devices()
        print(f"🔍 تم العثور على {len(devices)} جهاز في الشبكة")
        
        for device in devices:
            child_name = self.get_child_name_by_ip(device['ip_address'])
            if child_name:
                print(f"👶 مراقبة {child_name} على {device['ip_address']}")
                
                # مراقبة التطبيقات
                processes = self.monitor_processes(device['ip_address'])
                for proc in processes:
                    if proc['is_suspicious']:
                        print(f"⚠️ عملية مشبوهة: {proc['process_name']}")
                
                # مراقبة البحث
                searches = self.monitor_search_activities(device['ip_address'])
                for search in searches:
                    if search['is_inappropriate']:
                        print(f"🔍 بحث غير مناسب: {search['search_terms']}")
                
                # مراقبة المشاهدة
                viewing = self.monitor_viewing_activities(device['ip_address'])
                for view in viewing:
                    if view['is_blocked']:
                        print(f"🚫 محتوى محظور: {view['content_title']}")
        
        # إنشاء تقرير شامل
        report = self.generate_comprehensive_report()
        print("\n📊 التقرير الشامل:")
        print(f"   • الأجهزة المراقبة: {len(report['devices_monitored'])}")
        print(f"   • التطبيقات النشطة: {report['total_activities'].get('total_applications', 0)}")
        print(f"   • عمليات البحث: {report['total_activities'].get('total_searches', 0)}")
        print(f"   • المواقع المزارة: {report['total_activities'].get('total_visits', 0)}")
        
        return report

def main():
    """الدالة الرئيسية للاختبار"""
    print("🧪 اختبار النظام المحسن")
    print("=" * 50)
    
    # إنشاء النظام
    monitor = AdvancedParentalMonitor()
    
    # بدء المراقبة
    report = monitor.start_monitoring()
    
    print("\n✅ تم إنجاز المراقبة المتقدمة بنجاح!")
    return report

if __name__ == "__main__":
    main()