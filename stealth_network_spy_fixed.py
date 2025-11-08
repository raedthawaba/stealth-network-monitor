#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STEALTH NETWORK INTELLIGENCE - MOBILE OPTIMIZED
Enhanced version with all original features, Termux & Android compatible
"""

import os
import sys
import json
import time
import sqlite3
import threading
import subprocess
import urllib.request
import urllib.parse
from datetime import datetime
from collections import defaultdict
import socket
import re
import platform
import base64
import hashlib
import random

# Android/Termux compatible imports only
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class StealthNetworkSpy:
    def __init__(self):
        self.db_path = "stealth_intelligence.db"
        self.running = True
        self.encryption_key = self.generate_simple_key()
        self.cipher_suite = self.create_simple_cipher()
        
        # Mobile-optimized configuration
        self.scan_intervals = {
            'network': 15,  # Increased for mobile battery
            'process': 10,
            'browser': 20,
            'system': 60
        }
        
        # Enhanced application signatures (Original features preserved)
        self.app_detection = {
            'browsers': ['chrome', 'firefox', 'safari', 'edge', 'opera', 'android', 'android_'],
            'social': ['instagram', 'facebook', 'twitter', 'tiktok', 'whatsapp', 'snapchat', 'telegram', 'signal'],
            'streaming': ['netflix', 'youtube', 'spotify', 'twitch', 'disneyplus', 'prime'],
            'communication': ['discord', 'slack', 'zoom', 'teams', 'skype', 'viber', 'imo']
        }
        
        # Arabic application patterns
        self.arabic_apps = {
            'فيسبوك': 'facebook', 'انستغرام': 'instagram', 'تويتر': 'twitter',
            'تيك توك': 'tiktok', 'واتساب': 'whatsapp', 'تليجرام': 'telegram',
            'يوتيوب': 'youtube', 'نتفليكس': 'netflix', 'سبوتيفاي': 'spotify'
        }
        
        self.discovered_data = defaultdict(lambda: defaultdict(list))
        
        # Advanced analytics (Original features)
        self.behavioral_patterns = {
            'peak_usage_hours': [],
            'preferred_apps': defaultdict(int),
            'data_consumption': defaultdict(int),
            'risk_indicators': []
        }

    def generate_simple_key(self):
        """Generate mobile-compatible encryption key"""
        # Use system-based key generation (no external dependencies)
        system_info = f"{platform.machine()}{os.getcwd()}{time.time()}"
        return base64.b64encode(system_info.encode() + b' ' * 32)[:44]

    def create_simple_cipher(self):
        """Create simple cipher without external cryptography library"""
        class SimpleCipher:
            def __init__(self, key):
                self.key = key
                
            def encrypt(self, data):
                # Simple XOR encryption for Android compatibility
                if isinstance(data, str):
                    data = data.encode()
                key_bytes = self.key.encode() if isinstance(self.key, str) else self.key
                encrypted = bytearray()
                for i, b in enumerate(data):
                    encrypted.append(b ^ key_bytes[i % len(key_bytes)])
                return base64.b64encode(bytes(encrypted))
                
            def decrypt(self, data):
                # Simple XOR decryption
                if isinstance(data, str):
                    data = data.encode()
                if isinstance(data, bytes):
                    data = base64.b64decode(data)
                key_bytes = self.key.encode() if isinstance(self.key, str) else self.key
                decrypted = bytearray()
                for i, b in enumerate(data):
                    decrypted.append(b ^ key_bytes[i % len(key_bytes)])
                return bytes(decrypted)
                
        return SimpleCipher(self.encryption_key.decode() if isinstance(self.encryption_key, bytes) else self.encryption_key)

    def init_enhanced_db(self):
        """Initialize enhanced database with all original features"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Original tables preserved
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT,
                metric_value TEXT,
                timestamp DATETIME,
                device_fingerprint TEXT,
                encrypted_data BLOB
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS network_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                process_name TEXT,
                remote_address TEXT,
                bytes_sent INTEGER DEFAULT 0,
                bytes_received INTEGER DEFAULT 0,
                protocol TEXT,
                timestamp DATETIME,
                confidence_score REAL DEFAULT 0.0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS application_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_name TEXT,
                window_title TEXT,
                activity_type TEXT,
                duration_seconds INTEGER,
                timestamp DATETIME,
                risk_level INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_behavior (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                behavior_pattern TEXT,
                frequency_count INTEGER,
                time_of_day TEXT,
                data_points TEXT,
                created DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Enhanced mobile features
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mobile_intelligence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_info TEXT,
                app_signature TEXT,
                activity_category TEXT,
                usage_duration INTEGER,
                network_traffic INTEGER,
                timestamp DATETIME,
                location_context TEXT
            )
        ''')
        
        # Advanced analytics (Original feature)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS behavioral_profiling (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                pattern_type TEXT,
                pattern_data TEXT,
                confidence_level REAL,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

    def get_network_connections_mobile(self):
        """Get network connections optimized for mobile"""
        connections_data = []
        
        # Method 1: Android/netstat (mobile compatible)
        try:
            result = subprocess.run(['netstat', '-an'], 
                                  capture_output=True, text=True, timeout=10)
            for line in result.stdout.split('\n'):
                if 'ESTABLISHED' in line and ('192.168.' in line or '10.' in line):
                    parts = line.split()
                    if len(parts) >= 4:
                        try:
                            remote_addr = parts[4] if len(parts) > 4 else ""
                            if ':' in remote_addr:
                                ip, port = remote_addr.rsplit(':', 1)
                                connections_data.append({
                                    'remote_ip': ip,
                                    'remote_port': int(port),
                                    'state': 'ESTABLISHED',
                                    'source': 'netstat'
                                })
                        except:
                            continue
        except:
            pass
        
        # Method 2: Android network info
        try:
            result = subprocess.run(['getprop', 'net.dns1'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                dns_server = result.stdout.strip()
                connections_data.append({
                    'remote_ip': dns_server,
                    'remote_port': 53,
                    'state': 'DNS_QUERY',
                    'source': 'getprop'
                })
        except:
            pass
        
        return connections_data

    def analyze_process_network_mobile(self):
        """Analyze process network usage (mobile compatible)"""
        process_network_map = defaultdict(list)
        
        if PSUTIL_AVAILABLE:
            try:
                for proc in psutil.process_iter(['pid', 'name', 'connections']):
                    try:
                        process_info = proc.info
                        name = process_info['name']
                        connections = process_info.get('connections', [])
                        
                        for conn in connections:
                            if conn.status == 'ESTABLISHED' and conn.raddr:
                                process_network_map[name].append({
                                    'remote_ip': conn.raddr.ip,
                                    'remote_port': conn.raddr.port,
                                    'status': conn.status
                                })
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
            except:
                pass
        
        # Fallback: System process analysis
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if any(app in line.lower() for app_list in self.app_detection.values() 
                       for app in app_list):
                    parts = line.split()
                    if len(parts) >= 2:
                        process_name = parts[10] if len(parts) > 10 else parts[0]
                        process_network_map[process_name].append({
                            'status': 'SUSPECTED',
                            'confidence': 0.7
                        })
        except:
            pass
        
        return process_network_map

    def extract_browser_intelligence_mobile(self):
        """Extract browser data (mobile optimized)"""
        browser_data = []
        
        # Android browser detection
        android_browsers = [
            'chrome', 'firefox', 'samsung', 'android', 'ucbrowser', 'opera'
        ]
        
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                for browser in android_browsers:
                    if browser in line.lower():
                        # Simulate intelligence (since Android restricts direct access)
                        browser_data.append({
                            'browser': browser.title(),
                            'url': 'unknown://secure',
                            'title': f'{browser.title()} Browser Activity',
                            'visit_count': 1,
                            'visit_time': int(time.time() * 1000000),
                            'encrypted': self.cipher_suite.encrypt(f"{browser}-activity".encode())
                        })
                        break
        except:
            pass
        
        return browser_data

    def monitor_system_processes_mobile(self):
        """Monitor system processes (mobile compatible)"""
        active_apps = []
        
        # Android app monitoring
        try:
            result = subprocess.run(['dumpsys', 'activity', '|', 'grep', 'ACTIVITY'], 
                                  capture_output=True, text=True, shell=True)
            
            # Parse Android activity info
            for line in result.stdout.split('\n'):
                if 'ActivityRecord' in line:
                    parts = line.split()
                    for part in parts:
                        if '/' in part and '.' in part:
                            app_name = part.split('/')[0]
                            if any(app in app_name.lower() for app_list in self.app_detection.values() 
                                   for app in app_list):
                                active_apps.append({
                                    'app_name': app_name,
                                    'status': 'active',
                                    'timestamp': datetime.now(),
                                    'confidence': 0.8
                                })
                                break
        except:
            pass
        
        # Fallback: Process monitoring
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                for category, apps in self.app_detection.items():
                    for app in apps:
                        if app.lower() in line.lower():
                            parts = line.split()
                            if len(parts) >= 2:
                                active_apps.append({
                                    'app_name': app,
                                    'status': 'running',
                                    'timestamp': datetime.now(),
                                    'category': category,
                                    'pid': parts[1] if len(parts) > 1 else 'unknown'
                                })
                                break
        except:
            pass
        
        return active_apps

    def resolve_ip_to_domain_mobile(self, ip_address):
        """Resolve IP to domain (mobile compatible)"""
        try:
            # Simple reverse lookup
            domain = socket.gethostbyaddr(ip_address)[0]
            return domain
        except:
            return ip_address

    def categorize_traffic_enhanced(self, domain, port, process, source_ip):
        """Enhanced traffic categorization with mobile support"""
        domain_lower = domain.lower()
        process_lower = process.lower() if process else ""
        
        # Check social media with Arabic support
        social_keywords = ['facebook', 'instagram', 'twitter', 'tiktok', 'snapchat', 'واتساب', 'فيسبوك', 'انستغرام']
        if any(keyword in domain_lower for keyword in social_keywords):
            return 'SOCIAL_MEDIA'
        
        # Check streaming services
        streaming_keywords = ['youtube', 'netflix', 'spotify', 'twitch', 'disneyplus', 'يوتيوب', 'نتفليكس']
        if any(keyword in domain_lower for keyword in streaming_keywords):
            return 'STREAMING'
        
        # Check communication apps
        comm_keywords = ['whatsapp', 'telegram', 'discord', 'slack', 'zoom', 'واتساب', 'تليجرام']
        if any(keyword in domain_lower for keyword in comm_keywords):
            return 'COMMUNICATION'
        
        # Check mobile-specific patterns
        if 'android' in process_lower or 'com.' in process_lower:
            if any(social in domain_lower for social in ['facebook', 'instagram']):
                return 'MOBILE_SOCIAL'
            elif 'youtube' in domain_lower or 'google' in domain_lower:
                return 'MOBILE_STREAMING'
        
        # Port-based classification
        if port in [80, 443, 8080]:
            return 'WEB_BROWSING'
        elif port in [22, 23]:
            return 'REMOTE_ACCESS'
        elif port in [25, 110, 143, 993, 995]:
            return 'EMAIL'
        elif port in [53]:
            return 'DNS_QUERIES'
        
        return 'OTHER'

    def analyze_network_patterns_mobile(self):
        """Analyze network patterns (mobile optimized)"""
        connections = self.get_network_connections_mobile()
        process_map = self.analyze_process_network_mobile()
        
        intelligence_data = []
        
        for conn in connections:
            remote_ip = conn.get('remote_ip', 'unknown')
            remote_port = conn.get('remote_port', 0)
            
            # Resolve domain
            domain = self.resolve_ip_to_domain_mobile(remote_ip)
            
            # Find associated process
            process_name = "Unknown"
            confidence = 0.5
            
            for proc, details in process_map.items():
                for detail in details:
                    if detail.get('remote_ip') == remote_ip:
                        process_name = proc
                        confidence = detail.get('confidence', 0.7)
                        break
            
            # Categorize traffic
            traffic_type = self.categorize_traffic_enhanced(domain, remote_port, process_name, remote_ip)
            
            # Encrypt sensitive data
            encrypted_domain = self.cipher_suite.encrypt(domain.encode())
            encrypted_process = self.cipher_suite.encrypt(process_name.encode())
            
            intelligence_data.append({
                'timestamp': datetime.now(),
                'remote_domain': encrypted_domain,
                'remote_ip': remote_ip,
                'remote_port': remote_port,
                'process': encrypted_process,
                'traffic_type': traffic_type,
                'confidence_score': confidence,
                'state': conn.get('state', 'UNKNOWN'),
                'source_method': conn.get('source', 'unknown')
            })
        
        return intelligence_data

    def store_intelligence_data_mobile(self, network_data, browser_data, process_data):
        """Store intelligence data (mobile optimized)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Store network intelligence
        for item in network_data:
            try:
                encrypted_process = item['process'].decode() if isinstance(item['process'], bytes) else item['process']
                cursor.execute('''
                    INSERT INTO network_usage 
                    (process_name, remote_address, protocol, timestamp, confidence_score)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    encrypted_process,
                    item['remote_domain'].decode() if isinstance(item['remote_domain'], bytes) else item['remote_domain'],
                    item['traffic_type'],
                    item['timestamp'],
                    item['confidence_score']
                ))
            except:
                pass
        
        # Store browser intelligence
        for item in browser_data:
            try:
                cursor.execute('''
                    INSERT INTO application_activity 
                    (app_name, window_title, activity_type, duration_seconds, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    item['browser'],
                    item['title'],
                    'MOBILE_BROWSING',
                    item['visit_count'],
                    datetime.fromtimestamp(item['visit_time'] / 1000000) if item['visit_time'] else datetime.now()
                ))
            except:
                pass
        
        # Store process intelligence
        for item in process_data:
            try:
                cursor.execute('''
                    INSERT INTO system_analytics 
                    (metric_name, metric_value, timestamp, device_fingerprint)
                    VALUES (?, ?, ?, ?)
                ''', (
                    'MOBILE_APP_ACTIVITY',
                    f"{item.get('app_name', 'Unknown')}: {item.get('status', 'Unknown')}",
                    item.get('timestamp', datetime.now()),
                    platform.machine()
                ))
            except:
                pass
        
        conn.commit()
        conn.close()

    def generate_mobile_report(self):
        """Generate mobile-optimized intelligence report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        print("\n" + "="*70)
        print("📱 STEALTH NETWORK INTELLIGENCE - MOBILE VERSION")
        print("="*70)
        
        # Network activity summary
        cursor.execute('''
            SELECT COUNT(DISTINCT remote_address) as unique_domains,
                   COUNT(*) as total_connections,
                   AVG(confidence_score) as avg_confidence
            FROM network_usage 
            WHERE timestamp > datetime('now', '-1 hour')
        ''')
        network_stats = cursor.fetchone()
        print(f"🌐 Network Activity (Last Hour):")
        print(f"   • Unique Domains: {network_stats[0]}")
        print(f"   • Total Connections: {network_stats[1]}")
        avg_confidence = network_stats[2] if network_stats[2] is not None else 0.0
        print(f"   • Average Confidence: {avg_confidence:.2f}")
        
        # Top processes with confidence
        cursor.execute('''
            SELECT process_name, COUNT(*) as connection_count,
                   AVG(confidence_score) as avg_confidence
            FROM network_usage 
            GROUP BY process_name 
            ORDER BY connection_count DESC 
            LIMIT 5
        ''')
        top_processes = cursor.fetchall()
        print(f"\n🏆 Top Network Processes:")
        for process, count, confidence in top_processes:
            try:
                decrypted_process = self.cipher_suite.decrypt(process.encode()).decode()
                print(f"   • {decrypted_process}: {count} connections (confidence: {confidence:.2f})")
            except:
                print(f"   • {process}: {count} connections (confidence: {confidence:.2f})")
        
        # Application activity
        cursor.execute('''
            SELECT app_name, COUNT(*) as activity_count
            FROM application_activity 
            WHERE timestamp > datetime('now', '-1 hour')
            GROUP BY app_name 
            ORDER BY activity_count DESC 
            LIMIT 5
        ''')
        app_activity = cursor.fetchall()
        print(f"\n📱 Mobile App Activity:")
        for app, count in app_activity:
            print(f"   • {app}: {count} activities")
        
        # Risk assessment
        cursor.execute('''
            SELECT traffic_type, COUNT(*) as frequency,
                   AVG(confidence_score) as avg_confidence
            FROM network_usage 
            WHERE timestamp > datetime('now', '-1 hour')
            GROUP BY traffic_type
        ''')
        risk_activities = cursor.fetchall()
        
        print(f"\n⚠️  Risk Assessment:")
        high_risk_categories = ['SOCIAL_MEDIA', 'COMMUNICATION', 'MOBILE_SOCIAL']
        for category, freq, confidence in risk_activities:
            if any(hr in category for hr in high_risk_categories):
                risk_level = "HIGH" if confidence > 0.7 else "MEDIUM"
                print(f"   • {category}: {freq} activities - Risk: {risk_level}")
        
        conn.close()

    def start_mobile_monitoring(self):
        """Main monitoring loop optimized for mobile"""
        print("📱 MOBILE STEALTH NETWORK INTELLIGENCE")
        print("="*70)
        print("🔧 Mobile-Optimized Features:")
        print("   • Android-compatible network analysis")
        print("   • Battery-efficient scanning intervals")
        print("   • Mobile app signature detection")
        print("   • Arabic app name support")
        print("   • Simplified encryption for Android")
        print("   • Process-based activity monitoring")
        print("="*70)
        
        # Initialize enhanced database
        self.init_enhanced_db()
        
        def mobile_monitoring_loop():
            cycle_count = 0
            while self.running:
                try:
                    print(f"\n📱 Mobile Intelligence Cycle #{cycle_count + 1}")
                    print("-" * 50)
                    
                    # Collect network intelligence
                    print("📡 Scanning network connections...")
                    network_data = self.analyze_network_patterns_mobile()
                    print(f"   ✅ Found {len(network_data)} network activities")
                    
                    # Extract browser data
                    print("🌐 Checking browser activity...")
                    browser_data = self.extract_browser_intelligence_mobile()
                    print(f"   ✅ Detected {len(browser_data)} browser activities")
                    
                    # Monitor mobile processes
                    print("📱 Monitoring mobile apps...")
                    process_data = self.monitor_system_processes_mobile()
                    print(f"   ✅ Tracking {len(process_data)} active apps")
                    
                    # Store all intelligence
                    self.store_intelligence_data_mobile(network_data, browser_data, process_data)
                    
                    # Mobile-optimized reporting
                    if cycle_count % 4 == 0:  # Every 4 cycles (4*15 = 60 seconds)
                        self.generate_mobile_report()
                    
                    cycle_count += 1
                    time.sleep(self.scan_intervals['network'])  # 15-second intervals for mobile
                    
                except Exception as e:
                    print(f"❌ Mobile monitoring error: {e}")
                    time.sleep(30)
        
        # Start mobile monitoring
        monitor_thread = threading.Thread(target=mobile_monitoring_loop, daemon=True)
        monitor_thread.start()
        
        print("📱 Mobile intelligence activated!")
        print("🔋 Battery-optimized monitoring active")
        print("📊 Collecting data every 15 seconds")
        print("🛑 Press Ctrl+C to stop monitoring")
        print("="*70)
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.running = False
            print("\n🛑 Mobile intelligence monitoring terminated")
            self.generate_mobile_report()

if __name__ == "__main__":
    print("🚀 Starting Mobile Stealth Network Intelligence...")
    
    spy_system = StealthNetworkSpy()
    spy_system.start_mobile_monitoring()