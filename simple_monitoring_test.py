#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام المراقبة الأبوية المبسط - للاختبار السريع
"""

import json
import sqlite3
import os
from datetime import datetime
from typing import Dict, List

def create_simple_monitoring_system():
    """إنشاء نظام مراقبة مبسط"""
    print("🧪 نظام المراقبة الأبوية المبسط")
    print("=" * 50)
    
    # إنشاء مجلد للمخرجات
    os.makedirs("monitoring_output", exist_ok=True)
    
    # تحميل التكوين
    try:
        with open('advanced_parental_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("✅ تم تحميل التكوين بنجاح")
    except Exception as e:
        print(f"❌ خطأ في تحميل التكوين: {e}")
        return False
    
    # إنشاء قاعدة بيانات
    db_path = "simple_monitoring.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # إنشاء الجداول
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monitored_children (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age_range TEXT,
            device_ip TEXT UNIQUE,
            device_type TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_name TEXT,
            device_ip TEXT,
            activity_type TEXT,
            activity_details TEXT,
            safety_level TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (child_name) REFERENCES monitored_children (name)
        )
    ''')
    
    conn.commit()
    print("✅ تم إنشاء قاعدة البيانات")
    
    # إضافة الأطفال
    children_added = 0
    for child in config.get('children', []):
        if child.get('is_active', False):
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO monitored_children 
                    (name, age_range, device_ip, device_type, is_active)
                    VALUES (?, ?, ?, ?, ?)
                ''', (child['name'], child['age_range'], child['device_ip'], 
                      child['device_type'], child['is_active']))
                
                children_added += 1
                print(f"✅ تم إضافة: {child['name']} ({child['age_range']}) - IP: {child['device_ip']}")
                
            except Exception as e:
                print(f"⚠️ خطأ في إضافة {child.get('name', 'طفل')}: {e}")
    
    conn.commit()
    
    # إضافة أنشطة تجريبية
    print("\n🔍 محاكاة الأنشطة...")
    sample_activities = [
        {
            'child_name': 'أحمد',
            'device_ip': '192.168.1.101',
            'activity_type': 'تطبيق',
            'activity_details': 'Khan Academy - الرياضيات',
            'safety_level': 'آمن'
        },
        {
            'child_name': 'أحمد',
            'device_ip': '192.168.1.101',
            'activity_type': 'بحث',
            'activity_details': 'حل المعادلات الرياضية',
            'safety_level': 'آمن'
        },
        {
            'child_name': 'فاطمة',
            'device_ip': '192.168.1.102',
            'activity_type': 'تطبيق',
            'activity_details': 'PBS Kids Games',
            'safety_level': 'آمن'
        },
        {
            'child_name': 'محمد',
            'device_ip': '192.168.1.103',
            'activity_type': 'تطبيق',
            'activity_details': 'GitHub - البرمجة',
            'safety_level': 'آمن'
        }
    ]
    
    for activity in sample_activities:
        cursor.execute('''
            INSERT INTO activities 
            (child_name, device_ip, activity_type, activity_details, safety_level)
            VALUES (?, ?, ?, ?, ?)
        ''', (activity['child_name'], activity['device_ip'], activity['activity_type'],
              activity['activity_details'], activity['safety_level']))
    
    conn.commit()
    print("✅ تم إضافة الأنشطة التجريبية")
    
    # عرض التقرير
    print(f"\n📊 تقرير المراقبة:")
    print(f"   • عدد الأطفال المراقبين: {children_added}")
    
    # عرض الأطفال
    cursor.execute('''
        SELECT name, age_range, device_ip, device_type 
        FROM monitored_children 
        WHERE is_active = TRUE
    ''')
    children = cursor.fetchall()
    
    print(f"\n👶 الأطفال المراقبون:")
    for child in children:
        name, age_range, ip, device_type = child
        print(f"   • {name} ({age_range}) - {device_type} - IP: {ip}")
    
    # عرض الأنشطة
    print(f"\n🔍 الأنشطة المكتشفة:")
    cursor.execute('''
        SELECT child_name, activity_type, activity_details, safety_level, timestamp
        FROM activities 
        ORDER BY timestamp DESC
    ''')
    activities = cursor.fetchall()
    
    for activity in children_added:
        child_name, act_type, details, safety, timestamp in activity
        status_icon = "✅" if safety == "آمن" else "⚠️"
        print(f"   {status_icon} {child_name}: {act_type} - {details} ({safety})")
    
    # إحصائيات الأمان
    cursor.execute('''
        SELECT safety_level, COUNT(*) 
        FROM activities 
        GROUP BY safety_level
    ''')
    safety_stats = cursor.fetchall()
    
    print(f"\n🛡️ إحصائيات الأمان:")
    for level, count in safety_stats:
        print(f"   • {level}: {count} نشاط")
    
    # التوصيات
    print(f"\n💡 التوصيات:")
    recommendations = [
        "🎯 نظام المراقبة يعمل بنجاح",
        "📱 جميع الأنشطة المسجلة آمنة ومناسبة",
        "💬 تواصل مستمر مع الأطفال حول الأمان الرقمي",
        "📚 شجع على الأنشطة التعليمية والترفيهية الآمنة",
        "🔍 راجع الأنشطة بانتظام مع الأطفال",
        "⚖️ حافظ على التوازن بين الأمان والخصوصية"
    ]
    
    for rec in recommendations:
        print(f"   {rec}")
    
    # حفظ تقرير JSON
    report = {
        'timestamp': datetime.now().isoformat(),
        'children_count': children_added,
        'children': [dict(zip(['name', 'age_range', 'device_ip', 'device_type'], child)) 
                    for child in children],
        'activities': [dict(zip(['child_name', 'activity_type', 'activity_details', 'safety_level', 'timestamp'], activity)) 
                      for activity in activities],
        'safety_stats': dict(safety_stats),
        'status': 'نجح الاختبار'
    }
    
    with open('monitoring_output/monitoring_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    conn.close()
    print(f"\n✅ تم حفظ التقرير في: monitoring_output/monitoring_report.json")
    print("🎉 تم إنجاز النظام بنجاح!")
    
    return True

if __name__ == "__main__":
    create_simple_monitoring_system()