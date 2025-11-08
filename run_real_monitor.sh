cd ~/monitoring

# إيقاف أي مراقبة سابقة
pkill -f universal_monitor 2>/dev/null || true

# إنشاء مجلد جديد
mkdir -p ~/real_monitoring
cd ~/real_monitoring

# إنشاء نظام المراقبة الحقيقية
cat > real_monitor.py << 'EOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام المراقبة الحقيقية لجميع الأجهزة
يسجل الأنشطة الفعلية من الشبكة
"""

import sqlite3
import threading
import time
import os
import subprocess
import socket
import json
from datetime import datetime
import re
from collections import defaultdict

class RealNetworkMonitor:
    def __init__(self):
        self.db_path = "real_monitoring.db"
        self.running = True
        self.monitored_devices = {}
        self.active_connections = {}
        self.dns_cache = {}
        self.process_cache = {}
        
        # قائمة التطبيقات والمعروفة
        self.known_apps = {
            "chrome": "Google Chrome",
            "firefox": "Mozilla Firefox", 
            "safari": "Safari",
            "instagram": "Instagram",
            "tiktok": "TikTok",
            "whatsapp": "WhatsApp",
            "telegram": "Telegram",
            "facebook": "Facebook",
            "snapchat": "Snapchat",
            "youtube": "YouTube",
            "netflix": "Netflix",
            "spotify": "Spotify",
            "discord": "Discord",
            "twitter": "Twitter",
            "telegram": "Telegram"
        }
        
        # مواقع شائعة
        self.popular_sites = {
            "google.com": "محرك البحث Google",
            "youtube.com": "يوتيوب",
            "facebook.com": "فيسبوك", 
            "instagram.com": "إنستقرام",
            "whatsapp.com": "واتساب",
            "netflix.com": "نتفليكس",
            "tiktok.com": "تيك توك",
            "twitter.com": "تويتر",
            "snapchat.com": "سناب شات",
            "amazon.com": "أمازون",
            "wikipedia.org": "ويكيبيديا",
            "linkedin.com": "لينكد إن",
            "discord.com": "ديسكورد",
            "spotify.com": "سبوتيفاي"
        }
    
    def get_db_connection(self):
        """إنشاء اتصال جديد بقاعدة البيانات"""
        return sqlite3.connect(self.db_path, check_same_thread=False)
    
    def init_db(self):
        """إنشاء قاعدة البيانات والجداول"""
        conn = self.get_db_connection()
        try:
            cursor = conn.cursor()
            
            # جدول الأجهزة المتصلة
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip_address TEXT UNIQUE NOT NULL,
                    mac_address TEXT,
                    hostname TEXT,
                    first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
                    total_connections INTEGER DEFAULT 0
                )
            ''')
            
            # جدول الاتصالات الفعلية
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS real_connections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_ip TEXT NOT NULL,
                    source_port INTEGER,
                    dest_ip TEXT NOT NULL,
                    dest_port INTEGER,
                    protocol TEXT,
                    application_name TEXT,
                    website_domain TEXT,
                    connection_start DATETIME DEFAULT CURRENT_TIMESTAMP,
                    connection_end DATETIME,
                    data_sent INTEGER DEFAULT 0,
                    data_received INTEGER DEFAULT 0,
                    connection_status TEXT DEFAULT 'active'
                )
            ''')
            
            # جدول DNS requests
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dns_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_ip TEXT NOT NULL,
                    domain_name TEXT NOT NULL,
                    query_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    resolved_ip TEXT,
                    request_type TEXT
                )
            ''')
            
            # جدول التطبيقات المستخدمة
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS app_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_ip TEXT NOT NULL,
                    app_name TEXT NOT NULL,
                    process_name TEXT,
                    start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    end_time DATETIME,
                    data_usage INTEGER DEFAULT 0
                )
            ''')
            
            # جدول المواقع المزارة
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS website_visits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_ip TEXT NOT NULL,
                    domain_name TEXT NOT NULL,
                    full_url TEXT,
                    visit_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    duration_seconds INTEGER,
                    page_views INTEGER DEFAULT 1
                )
            ''')
            
            conn.commit()
            print("✅ قاعدة البيانات الحقيقية تم إنشاؤها بنجاح!")
        except sqlite3.Error as e:
            print(f"❌ خطأ في إنشاء قاعدة البيانات: {e}")
        finally:
            conn.close()
    
    def get_network_connections(self):
        """الحصول على جميع الاتصالات الشبكية النشطة"""
        try:
            result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True)
            connections = []
            
            for line in result.stdout.split('\n'):
                if ':' in line and not line.startswith('State'):
                    parts = line.split()
                    if len(parts) >= 4:
                        local_addr = parts[4] if len(parts) > 4 else ""
                        remote_addr = parts[5] if len(parts) > 5 else ""
                        
                        # تحليل العناوين
                        if ':' in local_addr and remote_addr != '*:*':
                            connections.append({
                                'local': local_addr,
                                'remote': remote_addr,
                                'state': parts[0] if parts else 'unknown'
                            })
            return connections
        except Exception as e:
            print(f"خطأ في جمع الاتصالات: {e}")
            return []
    
    def get_device_processes(self, device_ip):
        """الحصول على العمليات النشطة من الجهاز"""
        try:
            # محاولة الحصول على العمليات باستخدام netstat
            result = subprocess.run(['netstat', '-an'], capture_output=True, text=True)
            processes = []
            
            for line in result.stdout.split('\n'):
                if device_ip in line and 'ESTABLISHED' in line:
                    # تحليل العملية
                    parts = line.split()
                    if len(parts) >= 4:
                        local_addr = parts[3]
                        remote_addr = parts[4] if len(parts) > 4 else ""
                        
                        # استخراج المنفذ
                        try:
                            local_port = int(local_addr.split(':')[-1])
                            process_name = self.get_process_by_port(local_port)
                            if process_name:
                                processes.append({
                                    'port': local_port,
                                    'process': process_name,
                                    'remote': remote_addr
                                })
                        except:
                            continue
            
            return processes
        except Exception as e:
            print(f"خطأ في جمع العمليات: {e}")
            return []
    
    def get_process_by_port(self, port):
        """الحصول على اسم العملية بواسطة المنفذ"""
        # المنافذ الشائعة
        port_mapping = {
            80: "HTTP",
            443: "HTTPS", 
            53: "DNS",
            22: "SSH",
            21: "FTP",
            25: "SMTP",
            110: "POP3",
            143: "IMAP",
            993: "IMAPS",
            995: "POP3S",
            443: "HTTPS",
            8080: "HTTP-Proxy",
            3128: "HTTP-Proxy",
            1080: "SOCKS-Proxy"
        }
        
        if port in port_mapping:
            return port_mapping[port]
        
        # محاولة تحديد التطبيق من المنافذ
        app_ports = {
            1935: "RTMP/Streaming",
            5222: "XMPP/Jabber",
            6667: "IRC",
            7000: "AUDIO",
            8000: "Django/Gunicorn",
            3000: "Node.js",
            5000: "Flask/Python",
            9000: "Generic Service"
        }
        
        return app_ports.get(port, f"Port_{port}")
    
    def monitor_dns_requests(self):
        """مراقبة طلبات DNS"""
        try:
            # محاولة مراقبة DNS requests من logs
            dns_logs = []
            
            # فحص نظام DNS cache
            try:
                result = subprocess.run(['systemd-resolve', '--status'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'DNS Servers:' in line:
                        dns_servers = line.split('DNS Servers:')[1].split()
                        # هنا يمكن إضافة منطق لمراقبة DNS requests
            except:
                pass
            
            # محاولة مراقبة /var/log/syslog للـ DNS
            try:
                with open('/var/log/syslog', 'r') as f:
                    lines = f.readlines()[-100:]  # آخر 100 سطر
                    for line in lines:
                        if 'named' in line.lower() or 'dns' in line.lower():
                            dns_logs.append(line.strip())
            except:
                pass
            
            return dns_logs
        except Exception as e:
            print(f"خطأ في مراقبة DNS: {e}")
            return []
    
    def analyze_network_traffic(self):
        """تحليل حركة البيانات الحقيقية"""
        try:
            # الحصول على الاتصالات النشطة
            connections = self.get_network_connections()
            
            for conn in connections:
                try:
                    # تحليل العنوان المحلي
                    local_parts = conn['local'].split(':')
                    if len(local_parts) >= 2:
                        local_ip = ':'.join(local_parts[:-1])
                        local_port = int(local_parts[-1])
                        
                        # التحليل عن بُعد
                        remote_parts = conn['remote'].split(':')
                        if len(remote_parts) >= 2:
                            remote_ip = ':'.join(remote_parts[:-1])
                            remote_port = int(remote_parts[-1])
                            
                            # تحديد الجهاز
                            device_ip = local_ip
                            
                            # تحديد التطبيق
                            app_name = self.get_process_by_port(local_port)
                            
                            # تحديد الموقع
                            website_domain = self.resolve_ip_to_domain(remote_ip)
                            
                            # تسجيل الاتصال
                            self.log_real_connection(device_ip, local_port, remote_ip, remote_port, 
                                                   conn['state'], app_name, website_domain)
                
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"خطأ في تحليل حركة البيانات: {e}")
    
    def resolve_ip_to_domain(self, ip):
        """تحويل IP إلى اسم النطاق"""
        if ip in self.dns_cache:
            return self.dns_cache[ip]
        
        try:
            # محاولة الحصول على اسم النطاق من IP
            result = socket.gethostbyaddr(ip)
            domain = result[0] if result[0] else ip
        except:
            domain = ip
        
        self.dns_cache[ip] = domain
        return domain
    
    def log_real_connection(self, device_ip, source_port, dest_ip, dest_port, protocol, app_name, website_domain):
        """تسجيل الاتصال الحقيقي"""
        conn = self.get_db_connection()
        try:
            cursor = conn.cursor()
            
            # تحديث أو إضافة الجهاز
            cursor.execute('''
                INSERT OR REPLACE INTO devices (ip_address, last_seen, total_connections)
                VALUES (?, CURRENT_TIMESTAMP, 
                       COALESCE((SELECT total_connections FROM devices WHERE ip_address=?), 0) + 1)
            ''', (device_ip, device_ip))
            
            # تسجيل الاتصال الجديد
            cursor.execute('''
                INSERT INTO real_connections 
                (device_ip, source_port, dest_ip, dest_port, protocol, application_name, website_domain)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (device_ip, source_port, dest_ip, dest_port, protocol, app_name, website_domain))
            
            conn.commit()
            
            # عرض المعلومات
            website_info = self.popular_sites.get(website_domain, website_domain)
            app_info = self.known_apps.get(app_name.lower(), app_name)
            
            print(f"🌐 {device_ip}: {app_info} ← {website_info} (منفذ {dest_port})")
            
            # تسجيل الزيارة
            if website_domain != dest_ip:  # ليس IP مباشر
                self.log_website_visit(device_ip, website_domain)
            
            # تسجيل استخدام التطبيق
            if app_name and app_name != f"Port_{source_port}":
                self.log_app_usage(device_ip, app_name)
            
        except sqlite3.Error as e:
            print(f"خطأ في تسجيل الاتصال: {e}")
        finally:
            conn.close()
    
    def log_website_visit(self, device_ip, domain):
        """تسجيل زيارة الموقع"""
        conn = self.get_db_connection()
        try:
            cursor = conn.cursor()
            
            # التحقق من وجود زيارة حديثة
            cursor.execute('''
                SELECT id, visit_time FROM website_visits 
                WHERE device_ip = ? AND domain_name = ? 
                AND visit_time > datetime('now', '-2 minutes')
                ORDER BY visit_time DESC LIMIT 1
            ''', (device_ip, domain))
            
            existing = cursor.fetchone()
            
            if existing:
                # تحديث الزيارة الموجودة
                cursor.execute('''
                    UPDATE website_visits 
                    SET page_views = page_views + 1,
                        visit_time = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (existing[0],))
            else:
                # زيارة جديدة
                cursor.execute('''
                    INSERT INTO website_visits (device_ip, domain_name)
                    VALUES (?, ?)
                ''', (device_ip, domain))
            
            conn.commit()
        except sqlite3.Error as e:
            print(f"خطأ في تسجيل زيارة الموقع: {e}")
        finally:
            conn.close()
    
    def log_app_usage(self, device_ip, app_name):
        """تسجيل استخدام التطبيق"""
        conn = self.get_db_connection()
        try:
            cursor = conn.cursor()
            
            # التحقق من استخدام حديث
            cursor.execute('''
                SELECT id FROM app_usage 
                WHERE device_ip = ? AND app_name = ? 
                AND end_time IS NULL
                ORDER BY start_time DESC LIMIT 1
            ''', (device_ip, app_name))
            
            existing = cursor.fetchone()
            
            if not existing:
                # استخدام جديد
                cursor.execute('''
                    INSERT INTO app_usage (device_ip, app_name)
                    VALUES (?, ?)
                ''', (device_ip, app_name))
                conn.commit()
        except sqlite3.Error as e:
            print(f"خطأ في تسجيل استخدام التطبيق: {e}")
        finally:
            conn.close()
    
    def scan_discovered_devices(self):
        """فحص الأجهزة المكتشفة"""
        try:
            result = subprocess.run(['ip', 'neigh', 'show'], capture_output=True, text=True)
            devices = []
            
            for line in result.stdout.split('\n'):
                if 'REACHABLE' in line:
                    parts = line.split()
                    if 'lladdr' in parts and 'dev' in parts:
                        ip_idx = parts.index('dev') - 1
                        if ip_idx >= 0:
                            ip = parts[ip_idx]
                            mac = line.split('lladdr')[1].split()[0] if 'lladdr' in line else ""
                            devices.append({"ip": ip, "mac": mac})
            
            return devices
        except Exception as e:
            print(f"خطأ في فحص الأجهزة: {e}")
            return []
    
    def start_real_monitoring(self):
        """بدء المراقبة الحقيقية"""
        def monitoring_loop():
            while self.running:
                try:
                    # تحليل حركة البيانات الحقيقية
                    self.analyze_network_traffic()
                    
                    # مراقبة DNS requests
                    dns_requests = self.monitor_dns_requests()
                    for dns_log in dns_requests:
                        print(f"📡 DNS: {dns_log}")
                    
                    time.sleep(5)  # فحص كل 5 ثوان
                    
                except Exception as e:
                    print(f"خطأ في حلقة المراقبة: {e}")
                    time.sleep(5)
        
        # بدء خيط المراقبة
        monitor_thread = threading.Thread(target=monitoring_loop, daemon=True)
        monitor_thread.start()
    
    def start(self):
        """بدء النظام"""
        print("🔍 بدء نظام المراقبة الحقيقية")
        print("=" * 50)
        print("📡 المميزات:")
        print("  • مراقبة الاتصالات الفعلية")
        print("  • تحليل حركة البيانات الحقيقية")
        print("  • تسجيل المواقع المزارة فعلياً")
        print("  • مراقبة استخدام التطبيقات")
        print("  • تحليل طلبات DNS")
        print("=" * 50)
        
        # إنشاء قاعدة البيانات
        self.init_db()
        
        # فحص الأجهزة المتصلة
        devices = self.scan_discovered_devices()
        if devices:
            print(f"🔍 تم اكتشاف {len(devices)} جهاز:")
            for device in devices:
                print(f"  📱 {device['ip']} ({device['mac']})")
        
        # بدء المراقبة الحقيقية
        self.start_real_monitoring()
        
        print("=" * 50)
        print("🎯 المراقبة الحقيقية بدأت!")
        print("📊 لمراجعة البيانات:")
        print("  - الاتصالات: sqlite3 real_monitoring.db 'SELECT * FROM real_connections'")
        print("  - المواقع: sqlite3 real_monitoring.db 'SELECT * FROM website_visits'")
        print("  - التطبيقات: sqlite3 real_monitoring.db 'SELECT * FROM app_usage'")
        print("🛑 لإيقاف: Ctrl+C")
        print("=" * 50)
        
        try:
            while self.running:
                time.sleep(2)
        except KeyboardInterrupt:
            self.running = False
            print("\n🛑 تم إيقاف المراقبة الحقيقية")

if __name__ == "__main__":
    # بدء المراقبة
    monitor = RealNetworkMonitor()
    monitor.start()
EOF

# تشغيل النظام
echo "🚀 بدء تشغيل نظام المراقبة الحقيقية..."
python3 real_monitor.py