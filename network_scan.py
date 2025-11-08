#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import re
from datetime import datetime

class NetworkScanner:
    def __init__(self):
        self.devices = []
        self.local_ip = self.get_local_ip()
        
    def get_local_ip(self):
        """الحصول على عنوان IP المحلي"""
        try:
            result = subprocess.run(['hostname', '-I'], capture_output=True, text=True, check=True)
            return result.stdout.strip().split()[0]
        except:
            return "192.168.1.100"
    
    def get_network_range(self):
        """تحديد نطاق الشبكة للفحص"""
        local_parts = self.local_ip.split('.')
        if len(local_parts) >= 3:
            return f"{local_parts[0]}.{local_parts[1]}.{local_parts[2]}.0/24"
        return "192.168.1.0/24"
    
    def scan_devices(self):
        """فحص الأجهزة المتصلة على الشبكة"""
        print(f"🔍 بدء فحص الشبكة: {self.get_network_range()}")
        print("⏳ هذا قد يستغرق دقيقتين...")
        
        try:
            # استخدام nmap للفحص
            result = subprocess.run([
                'nmap', '-sn', self.get_network_range(), 
                '--max-rate=100', '-T4'
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                self.parse_nmap_output(result.stdout)
            else:
                # طريقة بديلة باستخدام ping
                self.scan_with_ping()
                
        except Exception as e:
            print(f"⚠️ خطأ في nmap: {e}")
            self.scan_with_ping()
    
    def parse_nmap_output(self, output):
        """تحليل ناتج nmap"""
        lines = output.split('\n')
        current_device = None
        
        for line in lines:
            line = line.strip()
            
            # البحث عن عنوان IP
            ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
            if ip_match:
                current_device = {
                    'ip': ip_match.group(1),
                    'name': 'غير معروف',
                    'mac': 'غير معروف',
                    'vendor': 'غير معروف'
                }
                self.devices.append(current_device)
                
            # البحث عن اسم المضيف
            host_match = re.search(r'Host is up\((.*?)\)', line)
            if host_match and current_device:
                current_device['name'] = host_match.group(1).strip()
    
    def scan_with_ping(self):
        """فحص بديل باستخدام ping"""
        network_base = self.get_network_range()[:self.get_network_range().rfind('.')] + '.'
        
        for i in range(1, 255):
            ip = f"{network_base}{i}"
            try:
                result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                                      capture_output=True, text=True, timeout=2)
                if result.returncode == 0:
                    device = {
                        'ip': ip,
                        'name': f'جهاز-{i}',
                        'mac': 'غير معروف',
                        'vendor': 'غير معروف'
                    }
                    self.devices.append(device)
                    print(f"✅ تم العثور على جهاز: {ip}")
            except:
                continue
    
    def get_device_info(self, ip):
        """الحصول على معلومات إضافية عن الجهاز"""
        try:
            # محاولة الحصول على اسم المضيف
            result = subprocess.run(['nslookup', ip], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                # استخراج اسم المضيف
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'name =' in line:
                        name = line.split('name =')[1].strip().rstrip('.')
                        return name
        except:
            pass
        return None
    
    def save_results(self):
        """حفظ النتائج في ملف JSON"""
        results = {
            'scan_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'local_ip': self.local_ip,
            'network_range': self.get_network_range(),
            'found_devices': len(self.devices),
            'devices': self.devices
        }
        
        with open('network_devices.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        return results
    
    def display_results(self, results):
        """عرض النتائج"""
        print("\n" + "="*60)
        print("📋 تقرير الأجهزة المكتشفة على الشبكة")
        print("="*60)
        print(f"🕒 وقت الفحص: {results['scan_time']}")
        print(f"🌐 عنوان IP المحلي: {results['local_ip']}")
        print(f"🔍 نطاق الشبكة: {results['network_range']}")
        print(f"📱 عدد الأجهزة المكتشفة: {results['found_devices']}")
        print("-"*60)
        
        if not results['devices']:
            print("❌ لم يتم العثور على أي أجهزة نشطة")
            print("💡 تأكد من:")
            print("   - اتصال WiFi يعمل")
            print("   -Devices موجودة على نفس الشبكة")
            print("   - Try running with internet connection")
        else:
            print("📱 الأجهزة المكتشفة:")
            for i, device in enumerate(results['devices'], 1):
                print(f"{i:2d}. IP: {device['ip']:<15} | الاسم: {device['name']}")
        
        print("="*60)
        print("💾 تم حفظ النتائج في ملف: network_devices.json")
        print("="*60)

def main():
    print("🌐 ماسح الشبكة للأطفال الحقيقيين")
    print("="*50)
    
    scanner = NetworkScanner()
    scanner.scan_devices()
    results = scanner.save_results()
    scanner.display_results(results)
    
    return results

if __name__ == "__main__":
    main()