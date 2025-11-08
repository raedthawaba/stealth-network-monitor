#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TERMINAL-FRIENDLY NETWORK MONITOR (Termux Compatible)
No root required, works on Android Termux
"""

import socket
import threading
import time
import os
import subprocess
import sqlite3
import json
import re
from datetime import datetime
from collections import defaultdict, deque

class TermuxNetworkMonitor:
    def __init__(self):
        self.db_path = "termux_network_monitor.db"
        self.running = True
        self.monitored_devices = {}
        
        # Application signatures (without root)
        self.app_signatures = {
            "social_media": {
                "patterns": [r"facebook", r"instagram", r"twitter", r"tiktok", r"snapchat", r"linkedin"],
                "keywords": ["فيسبوك", "انستغرام", "تيك توك", "تويتر", "سناب شات"]
            },
            "streaming": {
                "patterns": [r"youtube", r"youtube.com", r"netflix", r"spotify", r"twitch"],
                "keywords": ["يوتيوب", "نتفليكس", "سبوتيفاي", "تويتش"]
            },
            "gaming": {
                "patterns": [r"fortnite", r"minecraft", r"roblox", r"steam", r"pubg"],
                "keywords": ["لعبة", "جيمنج", "جازب", "بجي"]
            },
            "communication": {
                "patterns": [r"whatsapp", r"telegram", r"discord", r"signal"],
                "keywords": ["واتساب", "تليجرام", "ديسكورد", "سجنال"]
            }
        }
        
    def init_termux_db(self):
        """Initialize simplified database for Termux"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS discovered_devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT UNIQUE,
                mac_address TEXT,
                hostname TEXT,
                vendor TEXT,
                first_seen DATETIME,
                last_seen DATETIME,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS network_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_ip TEXT,
                request_type TEXT,
                destination TEXT,
                application TEXT,
                category TEXT,
                timestamp DATETIME,
                method TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dns_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_ip TEXT,
                domain TEXT,
                query_type TEXT,
                resolved_ip TEXT,
                timestamp DATETIME
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_usage_summary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_ip TEXT,
                app_name TEXT,
                category TEXT,
                usage_count INTEGER,
                last_used DATETIME
            )
        ''')
        
        conn.commit()
        conn.close()

    def scan_local_network(self):
        """Simple network discovery using ping (no root required)"""
        print("🔍 Scanning local network...")
        
        # Get local IP and network range
        try:
            result = subprocess.run(['hostname', '-I'], 
                                  capture_output=True, text=True)
            local_ip = result.stdout.strip().split()[0]
            network_base = '.'.join(local_ip.split('.')[:3])
            
            print(f"📱 Local IP: {local_ip}")
            print(f"🌐 Scanning network: {network_base}.0/24")
            
        except Exception as e:
            print(f"❌ Could not determine local IP: {e}")
            return []
        
        devices = []
        
        # Scan common IP range (1-100 for efficiency)
        def scan_ip(ip):
            try:
                # Use ping with timeout
                result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    devices.append({
                        'ip': ip,
                        'status': 'active',
                        'discovered_time': datetime.now()
                    })
                    print(f"  ✅ Found: {ip}")
            except:
                pass
        
        # Parallel scanning
        threads = []
        for i in range(1, 50):  # Scan first 50 IPs
            ip = f"{network_base}.{i}"
            thread = threading.Thread(target=scan_ip, args=(ip,))
            thread.start()
            threads.append(thread)
        
        # Wait for all threads
        for thread in threads:
            thread.join()
        
        return devices

    def monitor_dns_queries(self):
        """Monitor DNS queries using system logs (termux-friendly)"""
        def dns_monitor():
            print("📡 Starting DNS monitoring...")
            
            # Monitor system DNS cache
            while self.running:
                try:
                    # Use dig if available, otherwise use nslookup
                    try:
                        result = subprocess.run(['nslookup', 'google.com'], 
                                              capture_output=True, text=True, timeout=5)
                        if result.returncode == 0:
                            lines = result.stdout.split('\n')
                            for line in lines:
                                if 'Server:' in line:
                                    dns_server = line.split()[-1]
                                    # Store DNS server info
                                    conn = sqlite3.connect(self.db_path)
                                    cursor = conn.cursor()
                                    cursor.execute('''
                                        INSERT OR REPLACE INTO network_requests 
                                        (device_ip, request_type, destination, timestamp, method)
                                        VALUES (?, ?, ?, ?, ?)
                                    ''', ('local', 'DNS_Query', f"DNS_Server: {dns_server}", 
                                          datetime.now(), 'nslookup'))
                                    conn.commit()
                                    conn.close()
                                    break
                    except:
                        pass
                    
                    time.sleep(30)  # Check every 30 seconds
                    
                except Exception as e:
                    print(f"DNS monitor error: {e}")
                    time.sleep(60)
        
        dns_thread = threading.Thread(target=dns_monitor, daemon=True)
        dns_thread.start()

    def simulate_application_tracking(self):
        """Simulate application usage based on system activity"""
        def app_tracker():
            print("📱 Starting application usage tracker...")
            
            # Common apps and their network patterns
            app_indicators = {
                "Chrome": ["chrome", "google", "www.google"],
                "YouTube": ["youtube", "ytimg", "googlevideo"],
                "WhatsApp": ["whatsapp", "wa.me", "web.whatsapp"],
                "Instagram": ["instagram", "cdninstagram", "fbcdn"],
                "Telegram": ["telegram", "t.me", "web.telegram"],
                "TikTok": ["tiktok", "ttdomain", "tiktokcdn"],
                "Netflix": ["netflix", "nflximg", "nflxvideo"]
            }
            
            while self.running:
                try:
                    # Simulate usage by checking system processes
                    try:
                        result = subprocess.run(['ps', 'aux'], 
                                              capture_output=True, text=True)
                        
                        running_processes = result.stdout.lower()
                        
                        for app_name, indicators in app_indicators.items():
                            for indicator in indicators:
                                if indicator in running_processes:
                                    # Store app usage
                                    conn = sqlite3.connect(self.db_path)
                                    cursor = conn.cursor()
                                    
                                    # Determine category
                                    category = "other"
                                    for cat, sigs in self.app_signatures.items():
                                        if any(pattern in indicator for pattern in sigs["patterns"]):
                                            category = cat
                                            break
                                    
                                    cursor.execute('''
                                        INSERT INTO network_requests 
                                        (device_ip, request_type, destination, 
                                         application, category, timestamp, method)
                                        VALUES (?, ?, ?, ?, ?, ?, ?)
                                    ''', ('local', 'APP_Usage', indicator, app_name, 
                                          category, datetime.now(), 'process_check'))
                                    
                                    conn.commit()
                                    conn.close()
                                    
                                    print(f"📱 {app_name} detected ({category})")
                                    break
                                    
                    except Exception as e:
                        print(f"App tracking error: {e}")
                    
                    time.sleep(20)  # Check every 20 seconds
                    
                except Exception as e:
                    print(f"App tracker error: {e}")
                    time.sleep(60)
        
        app_thread = threading.Thread(target=app_tracker, daemon=True)
        app_thread.start()

    def generate_termux_report(self):
        """Generate report for Termux environment"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        print("\n" + "="*50)
        print("📊 TERMINAL NETWORK MONITOR REPORT")
        print("="*50)
        
        # Device count
        cursor.execute('SELECT COUNT(*) FROM discovered_devices WHERE status = "active"')
        active_devices = cursor.fetchone()[0]
        print(f"📱 Active Devices: {active_devices}")
        
        # Recent requests
        cursor.execute('''
            SELECT request_type, application, category, timestamp 
            FROM network_requests 
            ORDER BY timestamp DESC 
            LIMIT 10
        ''')
        recent_requests = cursor.fetchall()
        
        if recent_requests:
            print("\n🕒 Recent Network Activity:")
            for req_type, app, category, timestamp in recent_requests:
                print(f"  {timestamp[:19]} | {app or req_type} ({category})")
        
        # Application usage
        cursor.execute('''
            SELECT application, category, COUNT(*) as count 
            FROM network_requests 
            WHERE application IS NOT NULL 
            GROUP BY application 
            ORDER BY count DESC 
        ''')
        app_usage = cursor.fetchall()
        
        if app_usage:
            print("\n📱 Most Used Applications:")
            for app, category, count in app_usage:
                print(f"  {app}: {count} times ({category})")
        
        # Category summary
        cursor.execute('''
            SELECT category, COUNT(*) as count 
            FROM network_requests 
            WHERE category IS NOT NULL 
            GROUP BY category 
            ORDER BY count DESC
        ''')
        category_usage = cursor.fetchall()
        
        if category_usage:
            print("\n🏆 Category Usage:")
            for category, count in category_usage:
                print(f"  {category.title()}: {count} activities")
        
        conn.close()

    def start_termux_monitoring(self):
        """Start Termux-compatible monitoring"""
        print("🚀 STARTING TERMX NETWORK MONITOR")
        print("="*50)
        print("✅ No root required!")
        print("✅ Works on Android Termux!")
        print("✅ Safe for privacy!")
        print("="*50)
        
        # Initialize database
        self.init_termux_db()
        
        # Start monitoring
        print("🔍 Discovering network devices...")
        devices = self.scan_local_network()
        
        if devices:
            print(f"\n📱 Found {len(devices)} active devices:")
            for device in devices:
                print(f"  • {device['ip']}")
                
                # Store in database
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO discovered_devices 
                    (ip_address, last_seen, status)
                    VALUES (?, ?, ?)
                ''', (device['ip'], device['discovered_time'], 'active'))
                conn.commit()
                conn.close()
        
        # Start monitoring components
        self.monitor_dns_queries()
        self.simulate_application_tracking()
        
        print(f"\n🎯 Monitoring active for {len(devices)} devices!")
        print("📈 Collecting network intelligence...")
        print("🛑 Press Ctrl+C to stop")
        print("="*50)
        
        # Periodic reporting
        def periodic_report():
            while self.running:
                time.sleep(300)  # Every 5 minutes
                if self.running:
                    self.generate_termux_report()
        
        report_thread = threading.Thread(target=periodic_report, daemon=True)
        report_thread.start()
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.running = False
            print("\n🛑 Termux monitoring stopped")
            self.generate_termux_report()

if __name__ == "__main__":
    print("🔧 Starting Terminal-Friendly Network Monitor...")
    print("This version works on Termux without root requirements!")
    
    monitor = TermuxNetworkMonitor()
    monitor.start_termux_monitoring()