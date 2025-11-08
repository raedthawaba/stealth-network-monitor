#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
حلول مراقبة شبكة الأطفال - متى: 2025-11-08
يقدم حلول حقيقية لمراقبة حركة الإنترنت للأطفال
"""

import os
import sys
import time
import json
import sqlite3
from datetime import datetime
import subprocess

class NetworkMonitorSolutions:
    def __init__(self):
        self.solutions = {
            "dns_logging": {
                "name": "مراقبة DNS",
                "difficulty": "متوسط",
                "effectiveness": "جيد للمواقع",
                "description": "يسجل كل النطاقات التي يحاول الأطفال الوصول إليها"
            },
            "router_monitoring": {
                "name": "مراقبة الراوتر",
                "difficulty": "صعب",
                "effectiveness": "ممتاز",
                "description": "مراقبة كاملة لكل حركة الإنترنت"
            },
            "proxy_logging": {
                "name": "Proxy شفاف",
                "difficulty": "صعب",
                "effectiveness": "ممتاز",
                "description": "يسجل كل حركة HTTP/HTTPS"
            }
        }
    
    def check_router_info(self):
        """فحص معلومات الراوتر"""
        print("🔍 فحص معلومات الراوتر...")
        
        # فحص الراوتر الحالي
        try:
            # فحص البوابة
            result = subprocess.run(['ip', 'route', 'show', 'default'], 
                                  capture_output=True, text=True)
            default_route = result.stdout.strip()
            print(f"🛜 البوابة الافتراضية: {default_route}")
            
            # فحص DNS
            result = subprocess.run(['cat', '/etc/resolv.conf'], 
                                  capture_output=True, text=True)
            dns_servers = result.stdout
            print(f"🖥️ خوادم DNS: {dns_servers}")
            
            # فحص الأجهزة المتصلة
            result = subprocess.run(['ip', 'neigh'], 
                                  capture_output=True, text=True)
            neighbors = result.stdout
            print(f"📱 الأجهزة المتصلة:")
            print(neighbors)
            
        except Exception as e:
            print(f"❌ خطأ في فحص الراوتر: {e}")
    
    def create_dns_logging_solution(self):
        """إنشاء حل مراقبة DNS"""
        print("🌐 إنشاء حل مراقبة DNS...")
        
        dns_solution = """#!/bin/bash
# حل مراقبة DNS للأطفال
# يراقب كل النطاقات المزارة

# تثبيت dnsmasq للـ DNS logging
pkg install dnsmasq -y

# إنشاء ملف الإعدادات
cat > dnsmasq.conf << 'EOF'
# إعدادات مراقبة DNS
log-queries
log-facility=/data/data/com.termux/files/home/dns_queries.log
no-resolv
server=8.8.8.8
server=8.8.4.4
address=/#/8.8.8.8

# تسجيل النطاقات المشبوهة
log-queries-extra
EOF

# بدء dnsmasq
nohup dnsmasq -C dnsmasq.conf > /dev/null 2>&1 &

echo "✅ تم بدء مراقبة DNS"
echo "📄 السجلات محفوظة في: dns_queries.log"
echo "📊 لمراجعة آخر 50 طلب: tail -n 50 dns_queries.log"
"""
        
        with open("install_dns_monitor.sh", "w") as f:
            f.write(dns_solution)
        os.chmod("install_dns_monitor.sh", 0o755)
        
        print("✅ تم إنشاء: install_dns_monitor.sh")
    
    def create_router_monitoring_guide(self):
        """دليل مراقبة الراوتر"""
        print("📡 إنشاء دليل مراقبة الراوتر...")
        
        guide = """# دليل مراقبة الراوتر للأطفال

## الشرط المسبق:
1. راوتر يدعم OpenWrt أو DD-WRT
2. أو راوتر بسجلات TCPdump
3. صلاحيات إدارية على الراوتر

## حل OpenWrt (الأفضل):

### 1. تثبيت OpenWrt:
- ابحث عن model راوترك على: https://openwrt.org/
- اتبع دليل التثبيت

### 2. تثبيت برامج المراقبة:
```bash
opkg update
opkg install tcpdump tcpdump-analyze
opkg install logread
opkg install kmod-ipt-conntrack-extra
```

### 3. إعداد سجلات المراقبة:
```bash
# إنشاء ملف السجلات
touch /tmp/netmonitor.log
chmod 666 /tmp/netmonitor.log

# بدء tcpdump للتسجيل
tcpdump -i br-lan -n -s 0 -w /tmp/netmonitor.pcap &

# عرض في الوقت الفعلي
tail -f /tmp/netmonitor.log
```

### 4. تحليل البيانات:
```bash
# تحليل ملفات PCAP
tcpdump -r /tmp/netmonitor.pcap -n | grep -E "(google|youtube|instagram|tiktok)"
```

## حل DD-WRT:
- تفعيل "System Log" في الإدارة
- تعيين "Log Level" إلى "Debug"
- حفظ السجلات للـ syslog

## تحليل البيانات المرصودة:
```sql
-- قاعدة بيانات تحليل السجلات
CREATE TABLE net_logs (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    source_ip TEXT,
    dest_ip TEXT,
    dest_port INTEGER,
    protocol TEXT,
    domain TEXT
);
```
"""
        
        with open("router_monitoring_guide.md", "w") as f:
            f.write(guide)
        
        print("✅ تم إنشاء: router_monitoring_guide.md")
    
    def create_lan_scan_explain(self):
        """شرح سبب عدم عمل الفحص العادي"""
        print("🔍 إنشاء توضيح للمشكلة...")
        
        explain = """# لماذا لا يمكن مراقبة الأطفال من Termux؟

## المشكلة التقنية:
Termux على أندرويد (بدون روت) لا يستطيع:
- رؤية حركة الإنترنت من الأجهزة الأخرى
- فحص الحزم على الشبكة
- مراقبة DNS للأجهزة الأخرى

## ما يستطيع Termux فعله:
- ✅ كشف الأجهزة المتصلة (IP, MAC)
- ✅ رؤية اتصالات الجهاز الحالي
- ✅ فحص المنافذ المفتوحة
- ❌ مراقبة حركة الإنترنت للأطفال

## الحلول البديلة:
1. **مراقبة من الراوتر** - الوحيدة المتكاملة
2. **DNS Logging** - رؤية المواقع (وليس التطبيقات)
3. **Proxy مركزي** - يحتاج مهارات تقنية
4. **Per-device VPN** - يكسر شرط المخفية

## أفضل حل حالياً:
إذا كان راوترك يدعم OpenWrt، هذا هو الخيار الأمثل!
"""
        
        with open("why_termux_fails.md", "w") as f:
            f.write(explain)
        
        print("✅ تم إنشاء: why_termux_fails.md")
    
    def create_router_type_checker(self):
        """فحص نوع الراوتر"""
        print("📋 فحص نوع الراوتر...")
        
        checker = """#!/bin/bash
# فحص نوع الراوتر والميزات

echo "🔍 فحص الراوتر..."
echo "====================================="

# فحص الموديل
model=$(cat /sys/class/net/eth0/device 2>/dev/null | grep -o "vendor.*device.*" | head -1)
if [ -n "$model" ]; then
    echo "📱 موديل الراوتر: $model"
fi

# فحص IP الراوتر
router_ip=$(ip route | grep default | awk '{print $3}' | head -1)
echo "🖥️ IP الراوتر: $router_ip"

# فحص DNS
dns_ip=$(nslookup google.com | grep -A1 "Non-authoritative answer:" | tail -1 | awk '{print $3}')
if [ -n "$dns_ip" ]; then
    echo "🌐 DNS Server: $dns_ip"
fi

# اختبار اتصال بالراوتر
if ping -c 1 $router_ip > /dev/null 2>&1; then
    echo "✅ الراوتر متصل"
    
    # فحص Web Interface
    if curl -s http://$router_ip >/dev/null 2>&1; then
        echo "🌐 واجهة Web متاحة على: http://$router_ip"
    else
        echo "❌ واجهة Web غير متاحة"
    fi
    
else
    echo "❌ الراوتر غير متصل"
fi

echo "====================================="
echo "💡 للحصول على مراقبة حقيقية:"
echo "1. أدخل على واجهة الراوتر: http://$router_ip"
echo "2. ابحث عن 'Logs' أو 'System Log' أو 'OpenWrt'"
echo "3. إذا دعمت OpenWrt، يمكن تركيب برامج مراقبة"
"""
        
        with open("check_router.sh", "w") as f:
            f.write(checker)
        os.chmod("check_router.sh", 0o755)
        
        print("✅ تم إنشاء: check_router.sh")

def main():
    print("🚀 نظام حلول مراقبة شبكة الأطفال")
    print("=" * 50)
    
    solutions = NetworkMonitorSolutions()
    
    # فحص معلومات الراوتر
    solutions.check_router_info()
    
    print("\n📋 الخيارات المتاحة:")
    for key, solution in solutions.solutions.items():
        print(f"• {solution['name']}: {solution['description']}")
    
    print("\n🔧 إنشاء الحلول...")
    solutions.create_dns_logging_solution()
    solutions.create_router_monitoring_guide()
    solutions.create_lan_scan_explain()
    solutions.create_router_type_checker()
    
    print("\n📂 الملفات المنشأة:")
    print("• install_dns_monitor.sh - مراقبة DNS")
    print("• router_monitoring_guide.md - دليل الراوتر")
    print("• why_termux_fails.md - شرح المشكلة")
    print("• check_router.sh - فحص الراوتر")
    
    print("\n🎯 الخطوة التالية:")
    print("1. شغل: ./check_router.sh")
    print("2. ادخل على واجهة الراوتر")
    print("3. اختر الحل المناسب")

if __name__ == "__main__":
    main()