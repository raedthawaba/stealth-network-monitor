#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ اختبار سريع لنظام المراقبة الأبوية
"""

import json
import os
from datetime import datetime

def quick_test():
    """اختبار سريع"""
    print("⚡ اختبار سريع لنظام المراقبة الأبوية")
    print("=" * 50)
    
    # التحقق من الملفات
    files_to_check = [
        'parental_config.json',
        'advanced_parental_config.json', 
        'ParentalControlSystem.py',
        'advanced_parental_monitor.py',
        'parental_dashboard.html'
    ]
    
    print("📁 فحص الملفات:")
    for file in files_to_check:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - مفقود")
    
    # قراءة التكوين
    print(f"\n👶 الأطفال في النظام:")
    try:
        with open('parental_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        children = config.get('children', [])
        for child in children:
            if child.get('is_active', False):
                print(f"   👤 {child['name']} ({child['age_range']}) - {child['device_ip']}")
        
        print(f"\n📊 الإحصائيات:")
        print(f"   • عدد الأطفال: {len([c for c in children if c.get('is_active', False)])}")
        print(f"   • المواقع المسموحة: {len(config.get('web_filtering', {}).get('allowed_websites', []))}")
        print(f"   • المواقع المحظورة: {len(config.get('web_filtering', {}).get('blocked_domains', []))}")
        
    except Exception as e:
        print(f"   ❌ خطأ في قراءة التكوين: {e}")
    
    # محاكاة مراقبة بسيطة
    print(f"\n🔍 محاكاة المراقبة:")
    
    # أنشطة تجريبية
    activities = [
        ("أحمد", "استخدام Khan Academy", "آمن"),
        ("أحمد", "بحث عن 'math help'", "آمن"),
        ("فاطمة", "لعب ألعاب PBS Kids", "آمن"),
        ("محمد", "استخدام GitHub", "آمن"),
        ("محمد", "بحث عن 'python tutorial'", "آمن")
    ]
    
    for child, activity, safety in activities:
        icon = "✅" if safety == "آمن" else "⚠️"
        print(f"   {icon} {child}: {activity}")
    
    # التوصيات
    print(f"\n💡 التوصيات:")
    recommendations = [
        "🎯 جميع الأنشطة آمنة ومناسبة",
        "📚 الأطفال يستخدمون مواقع تعليمية",
        "🕐 راقب أوقات الاستخدام",
        "💬 تواصل مع الأطفال حول النشاط الرقمي",
        "🔄 قم بمراجعة أسبوعية للبيانات"
    ]
    
    for rec in recommendations:
        print(f"   {rec}")
    
    print(f"\n🎉 الاختبار السريع مكتمل!")
    print("💡 للتشغيل الكامل: python demo_parental_control.py")

if __name__ == "__main__":
    quick_test()