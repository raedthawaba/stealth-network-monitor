#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص أساسي للنظام - اختبار سريع
Basic System Check - Quick Test
"""

import os
import json
import sys
from datetime import datetime

def check_files():
    """فحص وجود الملفات الأساسية"""
    print("🔍 فحص وجود الملفات الأساسية...")
    
    required_files = [
        'ParentalControlSystem.py',
        'parental_config.json', 
        'advanced_parental_config.json',
        'parental_dashboard.html',
        'demo_parental_control.py'
    ]
    
    missing_files = []
    existing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            existing_files.append(file)
            print(f"✅ {file}")
        else:
            missing_files.append(file)
            print(f"❌ {file} - غير موجود")
    
    return len(missing_files) == 0, existing_files, missing_files

def check_config():
    """فصح إعدادات الأطفال"""
    print("\n👨‍👩‍👧‍👦 فحص إعدادات الأطفال...")
    
    try:
        with open('parental_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        if 'children' in config:
            children_count = len(config['children'])
            print(f"✅ عدد الأطفال المسجلين: {children_count}")
            
            for i, child in enumerate(config['children'], 1):
                name = child.get('name', 'غير محدد')
                age = child.get('age', 'غير محدد')
                device = child.get('device_ip', 'غير محدد')
                print(f"   {i}. {name} - عمر {age} سنة - جهاز: {device}")
            
            return True, children_count
        else:
            print("❌ لا توجد إعدادات أطفال في الملف")
            return False, 0
            
    except Exception as e:
        print(f"❌ خطأ في قراءة ملف الإعدادات: {e}")
        return False, 0

def check_database():
    """فحص قاعدة البيانات"""
    print("\n🗄️ فحص قاعدة البيانات...")
    
    if os.path.exists('parental_control.db'):
        try:
            size = os.path.getsize('parental_control.db')
            print(f"✅ قاعدة البيانات موجودة - الحجم: {size} بايت")
            return True
        except:
            print("❌ خطأ في فحص قاعدة البيانات")
            return False
    else:
        print("⚠️ قاعدة البيانات غير موجودة - سيتم إنشاؤها عند التشغيل")
        return False

def main():
    """الفحص الرئيسي"""
    print("=" * 60)
    print("🛡️ فحص سريع لنظام الرقابة الأبوية")
    print("🛡️ Parental Control System Quick Check")
    print("=" * 60)
    print(f"⏰ وقت الفحص: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # فحص الملفات
    files_ok, existing, missing = check_files()
    
    # فحص الإعدادات
    config_ok, children_count = check_config()
    
    # فحص قاعدة البيانات
    db_ok = check_database()
    
    # النتيجة النهائية
    print("\n" + "=" * 60)
    print("📊 نتائج الفحص:")
    print("=" * 60)
    
    if files_ok and config_ok:
        print("🎉 النظام جاهز للاستخدام!")
        print(f"👶 عدد الأطفال: {children_count}")
        print("📱 يمكن تشغيله على الكمبيوتر أو الهاتف")
        print("\n🚀 خطوات التشغيل:")
        print("1. للتشغيل التفاعلي: python3 ParentalControlSystem.py")
        print("2. للعرض التوضيحي: python3 demo_parental_control.py") 
        print("3. لفتح لوحة التحكم: افتح parental_dashboard.html في المتصفح")
        
    else:
        print("⚠️ النظام يحتاج إعدادات إضافية")
        if missing:
            print(f"ملفات مفقودة: {', '.join(missing)}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()