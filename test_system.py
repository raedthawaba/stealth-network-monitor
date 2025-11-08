#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار نظام المراقبة الأبوية بدون تفاعل
"""

import sys
import os
import json
import sqlite3
import time
import threading
from datetime import datetime
from typing import Dict, List, Optional

# إضافة المجلد الحالي للمسار
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from ParentalControlSystem import ParentalControlDashboard
    print("✅ تم استيراد نظام المراقبة بنجاح")
except ImportError as e:
    print(f"❌ خطأ في الاستيراد: {e}")
    sys.exit(1)

def test_system():
    """اختبار النظام باستخدام ملف التكوين"""
    print("🧪 اختبار نظام المراقبة الأبوية")
    print("=" * 40)
    
    # قراءة ملف التكوين
    try:
        with open('parental_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("✅ تم قراءة ملف التكوين بنجاح")
    except Exception as e:
        print(f"❌ خطأ في قراءة ملف التكوين: {e}")
        return False
    
    # إنشاء لوحة التحكم
    try:
        dashboard = ParentalControlDashboard()
        print("✅ تم إنشاء لوحة التحكم")
    except Exception as e:
        print(f"❌ خطأ في إنشاء لوحة التحكم: {e}")
        return False
    
    # إضافة الأطفال من ملف التكوين
    children_added = 0
    for child in config.get('children', []):
        try:
            if child.get('is_active', False):
                dashboard.add_child_device(
                    device_ip=child['device_ip'],
                    child_name=child['name'],
                    age_range=child['age_range'],
                    device_type=child['device_type']
                )
                children_added += 1
                print(f"✅ تم إضافة: {child['name']} (IP: {child['device_ip']})")
        except Exception as e:
            print(f"⚠️ خطأ في إضافة {child.get('name', 'طفل غير محدد')}: {e}")
    
    print(f"\n📊 عدد الأطفال المضافين: {children_added}")
    
    # اختبار قاعدة البيانات
    try:
        dashboard.database.get_all_devices()
        print("✅ اختبار قاعدة البيانات: نجح")
    except Exception as e:
        print(f"❌ خطأ في قاعدة البيانات: {e}")
        return False
    
    # اختبار التوصيات
    try:
        recommendations = dashboard.get_recommendations()
        print("✅ اختبار التوصيات: نجح")
        print("💡 التوصيات:")
        for rec in recommendations:
            print(f"   {rec}")
    except Exception as e:
        print(f"❌ خطأ في التوصيات: {e}")
        return False
    
    # اختبار عرض لوحة التحكم (بدون بدء المراقبة)
    try:
        print("\n🖥️ عرض لوحة التحكم...")
        dashboard.show_dashboard()
        print("✅ عرض لوحة التحكم: نجح")
    except Exception as e:
        print(f"❌ خطأ في عرض لوحة التحكم: {e}")
        return False
    
    print("\n🎉 جميع الاختبارات نجحت!")
    return True

if __name__ == "__main__":
    success = test_system()
    if success:
        print("\n✅ النظام جاهز للاستخدام")
        print("💡 لتشغيل المراقبة الفعلية، استخدم:")
        print("   python ParentalControlSystem.py")
    else:
        print("\n❌ توجد أخطاء في النظام")
        print("🔧 يرجى مراجعة الأخطاء أعلاه")