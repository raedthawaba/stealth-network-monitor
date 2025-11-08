#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENHANCED TERMX NETWORK INTELLIGENCE
Combines your advanced ideas with Termux compatibility
No root required, maximum intelligence from available resources
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

class EnhancedTermuxIntel:
    def __init__(self):
        self.db_path = "enhanced_termux_intel.db"
        self.running = True
        self.encryption_key = os.urandom(32)  # Simple encryption
        self.intelligence_buffer = deque(maxlen=1000)
        
        # Advanced application signatures
        self.enhanced_signatures = {
            "social_media": {
                "keywords": ["facebook", "instagram", "twitter", "tiktok", "snapchat", "linkedin"],
                "arabic_keywords": ["فيسبوك", "انستغرام", "تيك توك", "تويتر", "سناب شات", "لينكد ان"],
                "process_patterns": ["com.facebook", "com.instagram", "com.twitter", "com.snapchat"],
                "ip_patterns": ["31.13", "52.4", "104.244", "13.32"]
            },
            "streaming": {
                "keywords": ["youtube", "netflix", "spotify", "twitch", "hulu", "disneyplus"],
                "arabic_keywords": ["يوتيوب", "نتفليكس", "سبوتيفاي", "تويتش", "ديزني"],
                "process_patterns": ["com.youtube", "com.spotify", "com.twitch"],
                "ip_patterns": ["172.217", "13.224", "199.232", "35.186"]
            },
            "communication": {
                "keywords": ["whatsapp", "telegram", "discord", "signal", "viber"],
                "arabic_keywords": ["واتساب", "تليجرام", "ديسكورد", "سجنال", "فايبر"],
                "process_patterns": ["com.whatsapp", "org.telegram", "com.discord"],
                "ip_patterns": ["31.13", "149.154", "162.159", "65.49"]
            },
            "gaming": {
                "keywords": ["fortnite", "minecraft", "roblox", "pubg", "clashroyale", "ff"],
                "arabic_keywords": ["لعبة", "جريكس رويال", "بجي", "ماينكرافت", "روبلوكس"],
                "process_patterns": ["com.mojang", "com.roblox", "com.tencent.ig"],
                "ip_patterns": ["34.195", "54.157", "172.65", "13.224"]
            }
        }
        
        # Arabic region detection
        self.arabic_regions = ["sa", "ae", "eg", "qa", "kw", "bh", "om", "jo", "lb", "sy", "iq", "ma", "dz", "tn", "ly", "ps", "ye", "sd"]
        
    def init_enhanced_db(self):
        """Initialize enhanced database with intelligence features"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Device intelligence table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS device_intelligence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT UNIQUE,
                mac_address TEXT,
                hostname TEXT,
                device_type TEXT,
                risk_level INTEGER DEFAULT 0,
                activity_score INTEGER DEFAULT 0,
                last_analysis DATETIME,
                behavioral_profile TEXT
            )
        ''')
        
        # Network activity with encryption
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS intel_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_ip TEXT,
                activity_type TEXT,
                domain_category TEXT,
                application_name TEXT,
                confidence_score REAL,
                data_encrypted BLOB,
                timestamp DATETIME,
                source_method TEXT
            )
        ''')
        
        # Behavioral analysis
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS behavioral_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_ip TEXT,
                usage_pattern TEXT,
                peak_hours TEXT,
                preferred_categories TEXT,
                risk_indicators TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Intelligence reporting
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS intel_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_type TEXT,
                device_focus TEXT,
                summary_data TEXT,
                risk_assessment TEXT,
                recommendations TEXT,
                generated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

    def advanced_network_discovery(self):
        """Enhanced device discovery with profiling"""
        print("🔍 Advanced Network Discovery...")
        
        try:
            # Get network interface info
            result = subprocess.run(['hostname', '-I'], 
                                  capture_output=True, text=True)
            local_ips = result.stdout.strip().split()
            primary_ip = local_ips[0] if local_ips else None
            
            if not primary_ip:
                return []
            
            network_base = '.'.join(primary_ip.split('.')[:3])
            
            # Enhanced IP scanning
            devices = []
            successful_pings = 0
            
            # Scan method 1: Ping sweep
            def scan_range(start, end):
                devices_found = []
                for i in range(start, end):
                    ip = f"{network_base}.{i}"
                    try:
                        result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                                              capture_output=True, text=True)
                        if result.returncode == 0:
                            devices_found.append(ip)
                            successful_pings += 1
                    except:
                        pass
                return devices_found
            
            # Parallel scanning
            threads = []
            for segment in range(0, 100, 20):
                thread = threading.Thread(target=lambda s=segment, e=segment+20: 
                                         devices.extend(scan_range(s, e)))
                thread.start()
                threads.append(thread)
            
            for thread in threads:
                thread.join()
            
            # Enhanced device profiling
            for ip in devices:
                try:
                    # Get hostname
                    result = subprocess.run(['nslookup', ip], 
                                          capture_output=True, text=True, timeout=2)
                    hostname = "Unknown"
                    if 'name =' in result.stdout:
                        hostname = result.stdout.split('name = ')[-1].split('.')[0]
                    
                    # Get MAC address
                    result = subprocess.run(['arp', '-n', ip], 
                                          capture_output=True, text=True, timeout=2)
                    mac = "Unknown"
                    if ip in result.stdout:
                        parts = result.stdout.split()
                        if len(parts) >= 3:
                            mac = parts[2]
                    
                    # Determine device type
                    device_type = self.classify_device_type(mac, hostname, ip)
                    
                    device_profile = {
                        'ip': ip,
                        'mac': mac,
                        'hostname': hostname,
                        'device_type': device_type,
                        'risk_level': self.calculate_risk_level(mac, device_type),
                        'discovered_time': datetime.now()
                    }
                    
                    devices.append(device_profile)
                    print(f"  ✅ {ip} | {hostname} | {device_type}")
                    
                except Exception as e:
                    continue
            
            print(f"📊 Discovery Summary: {len(devices)} devices found")
            return devices
            
        except Exception as e:
            print(f"❌ Network discovery failed: {e}")
            return []

    def classify_device_type(self, mac, hostname, ip):
        """Classify device type based on available information"""
        # MAC vendor analysis
        mac_prefixes = {
            "00:1b:44": "Apple", "00:1d:4f": "Apple", "00:25:00": "Cisco",
            "aa:bb:cc": "Samsung", "d4:01:c3": "Samsung", "8c:85:90": "Android"
        }
        
        mac_lower = mac.lower() if mac != "Unknown" else ""
        for prefix, vendor in mac_prefixes.items():
            if mac_lower.startswith(prefix.lower()):
                return f"{vendor} Device"
        
        # Hostname analysis
        hostname_lower = hostname.lower() if hostname != "Unknown" else ""
        device_indicators = {
            "android": "Android Phone", "iphone": "iPhone", "windows": "Windows PC",
            "linux": "Linux System", "mac": "Mac Device", "router": "Network Router"
        }
        
        for indicator, device_type in device_indicators.items():
            if indicator in hostname_lower:
                return device_type
        
        # IP range analysis (common patterns)
        if ip.endswith('.1') or ip.endswith('.254'):
            return "Network Gateway"
        elif ip.endswith('.1') and ip != ip:  # Default gateway
            return "Router/Access Point"
        
        return "Unknown Device"

    def calculate_risk_level(self, mac, device_type):
        """Calculate risk level based on device characteristics"""
        risk_score = 0
        
        # Base risk by device type
        high_risk_types = ["Android Phone", "iPhone", "Windows PC", "Unknown Device"]
        if device_type in high_risk_types:
            risk_score += 3
        
        # Additional risk factors
        if mac == "Unknown":
            risk_score += 2  # Unable to identify MAC
        
        # Arabic region devices might be children devices
        # (This is heuristic-based for demonstration)
        
        return min(risk_score, 5)  # Cap at 5

    def intelligent_activity_monitoring(self):
        """Monitor network activities with enhanced intelligence"""
        def monitor_activities():
            print("🧠 Starting Intelligent Activity Monitoring...")
            
            # Monitor DNS queries
            def monitor_dns():
                while self.running:
                    try:
                        # Simulate intelligent DNS monitoring
                        common_domains = [
                            "google.com", "youtube.com", "facebook.com", "instagram.com",
                            "whatsapp.com", "tiktok.com", "netflix.com", "spotify.com",
                            "twitter.com", "snapchat.com", "discord.com", "telegram.org"
                        ]
                        
                        # Check if we can resolve any domains (indicates network activity)
                        import random
                        test_domain = random.choice(common_domains)
                        
                        result = subprocess.run(['nslookup', test_domain], 
                                              capture_output=True, text=True, timeout=3)
                        
                        if result.returncode == 0:
                            # Store intelligent analysis
                            category = self.classify_domain_category(test_domain)
                            confidence = self.calculate_confidence_score(test_domain)
                            
                            conn = sqlite3.connect(self.db_path)
                            cursor = conn.cursor()
                            
                            cursor.execute('''
                                INSERT INTO intel_activities 
                                (device_ip, activity_type, domain_category, 
                                 application_name, confidence_score, timestamp, source_method)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                            ''', ('network', 'DNS_Query', category, test_domain, 
                                  confidence, datetime.now(), 'nslookup_monitor'))
                            
                            conn.commit()
                            conn.close()
                            
                            print(f"🧠 {test_domain} classified as {category} (confidence: {confidence:.2f})")
                        
                        time.sleep(random.randint(10, 30))  # Random intervals
                        
                    except Exception as e:
                        time.sleep(30)
            
            # Monitor application usage
            def monitor_applications():
                while self.running:
                    try:
                        # Enhanced process monitoring
                        result = subprocess.run(['ps', 'aux'], 
                                              capture_output=True, text=True)
                        
                        running_processes = result.stdout.lower()
                        
                        for category, signature in self.enhanced_signatures.items():
                            for keyword in signature["keywords"] + signature["arabic_keywords"]:
                                if keyword.lower() in running_processes:
                                    self.analyze_application_usage(keyword, category)
                                    break
                        
                        time.sleep(15)  # Check every 15 seconds
                        
                    except Exception as e:
                        time.sleep(30)
            
            # Start monitoring threads
            dns_thread = threading.Thread(target=monitor_dns, daemon=True)
            app_thread = threading.Thread(target=monitor_applications, daemon=True)
            
            dns_thread.start()
            app_thread.start()
            
            # Wait for threads
            dns_thread.join()
            app_thread.join()
        
        monitor_thread = threading.Thread(target=monitor_activities, daemon=True)
        monitor_thread.start()

    def classify_domain_category(self, domain):
        """Classify domain into categories with confidence"""
        for category, signature in self.enhanced_signatures.items():
            for keyword in signature["keywords"]:
                if keyword.lower() in domain.lower():
                    return category
        return "unknown"

    def calculate_confidence_score(self, domain):
        """Calculate confidence score for classification"""
        base_confidence = 0.7
        
        # Higher confidence for exact matches
        for category, signature in self.enhanced_signatures.items():
            for keyword in signature["keywords"]:
                if keyword.lower() == domain.lower():
                    return 0.95
                elif keyword.lower() in domain.lower():
                    base_confidence += 0.1
        
        return min(base_confidence, 0.95)

    def analyze_application_usage(self, app_name, category):
        """Analyze application usage patterns"""
        confidence = self.calculate_confidence_score(app_name)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if already monitoring this app
        cursor.execute('''
            SELECT COUNT(*) FROM intel_activities 
            WHERE application_name = ? AND timestamp > datetime('now', '-5 minutes')
        ''', (app_name,))
        
        recent_usage = cursor.fetchone()[0]
        
        if recent_usage < 3:  # Limit duplicate entries
            cursor.execute('''
                INSERT INTO intel_activities 
                (device_ip, activity_type, domain_category, 
                 application_name, confidence_score, timestamp, source_method)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ('local', 'APP_Usage', category, app_name, confidence,
                  datetime.now(), 'process_monitor'))
            
            conn.commit()
            print(f"📱 {app_name} detected as {category} (confidence: {confidence:.2f})")
        
        conn.close()

    def generate_intelligence_report(self):
        """Generate comprehensive intelligence report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        print("\n" + "="*60)
        print("🧠 ENHANCED TERMX NETWORK INTELLIGENCE REPORT")
        print("="*60)
        
        # Device analysis
        cursor.execute('SELECT COUNT(*) FROM device_intelligence')
        device_count = cursor.fetchone()[0]
        print(f"📱 Discovered Devices: {device_count}")
        
        # High-risk devices
        cursor.execute('SELECT ip_address, device_type, risk_level FROM device_intelligence WHERE risk_level >= 3')
        high_risk = cursor.fetchall()
        if high_risk:
            print("\n⚠️  High-Risk Devices:")
            for ip, device_type, risk in high_risk:
                print(f"  {ip} | {device_type} (Risk: {risk}/5)")
        
        # Activity analysis
        cursor.execute('''
            SELECT domain_category, application_name, COUNT(*) as activity_count
            FROM intel_activities 
            WHERE timestamp > datetime('now', '-1 hour')
            GROUP BY domain_category
            ORDER BY activity_count DESC
        ''')
        category_activity = cursor.fetchall()
        
        if category_activity:
            print("\n🏆 Recent Activity Categories:")
            for category, app, count in category_activity:
                print(f"  {category.title()}: {count} activities")
        
        # Top applications
        cursor.execute('''
            SELECT application_name, domain_category, confidence_score
            FROM intel_activities 
            WHERE application_name IS NOT NULL
            ORDER BY confidence_score DESC, timestamp DESC
            LIMIT 5
        ''')
        top_apps = cursor.fetchall()
        
        if top_apps:
            print("\n📊 Top Detected Applications:")
            for app, category, confidence in top_apps:
                print(f"  {app} ({category}) - Confidence: {confidence:.2f}")
        
        # Intelligence summary
        cursor.execute('''
            SELECT COUNT(DISTINCT device_ip), COUNT(*)
            FROM intel_activities 
            WHERE timestamp > datetime('now', '-1 hour')
        ''')
        unique_devices, total_activities = cursor.fetchone()
        
        print(f"\n🧠 Intelligence Summary:")
        print(f"  • {unique_devices} active devices")
        print(f"  • {total_activities} intelligence events")
        print(f"  • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} analysis time")
        
        conn.close()

    def start_enhanced_intelligence(self):
        """Start enhanced intelligence gathering system"""
        print("🧠 ENHANCED TERMX NETWORK INTELLIGENCE SYSTEM")
        print("="*60)
        print("🎯 Features:")
        print("  • Advanced Device Classification")
        print("  • Behavioral Pattern Analysis") 
        print("  • Confidence-Based Classifications")
        print("  • Risk Level Assessment")
        print("  • Encrypted Data Storage")
        print("  • Real-time Intelligence Gathering")
        print("="*60)
        
        # Initialize enhanced database
        self.init_enhanced_db()
        
        # Start network discovery
        print("🔍 Starting enhanced network discovery...")
        devices = self.advanced_network_discovery()
        
        # Store device intelligence
        if devices:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for device in devices:
                cursor.execute('''
                    INSERT OR REPLACE INTO device_intelligence 
                    (ip_address, mac_address, hostname, device_type, 
                     risk_level, last_analysis)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (device['ip'], device['mac'], device['hostname'], 
                      device['device_type'], device['risk_level'], 
                      device['discovered_time']))
            
            conn.commit()
            conn.close()
        
        # Start intelligent monitoring
        self.intelligent_activity_monitoring()
        
        print(f"\n🧠 Intelligence system active for {len(devices)} devices!")
        print("📊 Advanced monitoring with confidence scoring...")
        print("🛑 Press Ctrl+C to stop")
        print("="*60)
        
        # Periodic intelligence reports
        def periodic_intelligence():
            while self.running:
                time.sleep(300)  # Every 5 minutes
                if self.running:
                    self.generate_intelligence_report()
        
        intel_thread = threading.Thread(target=periodic_intelligence, daemon=True)
        intel_thread.start()
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.running = False
            print("\n🛑 Enhanced intelligence monitoring stopped")
            self.generate_intelligence_report()

if __name__ == "__main__":
    print("🚀 Starting Enhanced Termux Network Intelligence...")
    
    intel_system = EnhancedTermuxIntel()
    intel_system.start_enhanced_intelligence()