#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار النظام المحسن - نسخة مستقلة
"""

import json
import sqlite3
import time
from datetime import datetime
from typing import Dict, List

def test_advanced_monitoring():
    """اختبار النظام المحسن"""
    print("🧪 اختبار النظام المحسن للمراقبة الأبوية")
    print("=" * 60)
    
    # تحميل التكوين المحسن
    try:
        with open('advanced_parental_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("✅ تم تحميل التكوين المحسن")
    except Exception as e:
        print(f"❌ خطأ في تحميل التكوين: {e}")
        return False
    
    # إنشاء قاعدة البيانات
    db_path = "test_monitoring.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # إنشاء الجداول
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            child_name TEXT,
            device_type TEXT,
            is_active BOOLEAN,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_ip TEXT,
            activity_type TEXT,
            details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_safe BOOLEAN
        )
    ''')
    
    conn.commit()
    print("✅ تم إنشاء قاعدة البيانات التجريبية")
    
    # إضافة الأطفال من التكوين
    children_added = 0
    for child in config.get('children', []):
        if child.get('is_active', False):
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO test_devices 
                    (ip_address, child_name, device_type, is_active)
                    VALUES (?, ?, ?, ?)
                ''', (child['device_ip'], child['name'], child['device_type'], True))
                
                # محاكاة أنشطة الطفل
                activities = simulate_child_activities(child)
                for activity in activities:
                    cursor.execute('''
                        INSERT INTO test_activities 
                        (device_ip, activity_type, details, is_safe)
                        VALUES (?, ?, ?, ?)
                    ''', (activity['device_ip'], activity['type'], 
                          activity['details'], activity['safe']))
                
                children_added += 1
                print(f"✅ تم إضافة: {child['name']} ({child['device_type']}) - IP: {child['device_ip']}")
                
            except Exception as e:
                print(f"⚠️ خطأ في إضافة {child.get('name', 'طفل')}: {e}")
    
    conn.commit()
    print(f"\n📊 عدد الأطفال المضافين: {children_added}")
    
    # عرض الأنشطة المكتشفة
    print("\n🔍 الأنشطة المكتشفة:")
    cursor.execute('''
        SELECT d.child_name, d.device_type, a.activity_type, a.details, a.is_safe
        FROM test_devices d
        JOIN test_activities a ON d.ip_address = a.device_ip
        ORDER BY a.timestamp DESC
    ''')
    
    activities = cursor.fetchall()
    for activity in activities:
        child_name, device_type, act_type, details, is_safe = activity
        status = "✅ آمن" if is_safe else "⚠️ يحتاج انتباه"
        print(f"   👶 {child_name} ({device_type}): {act_type} - {details} - {status}")
    
    # تحليل الأمان
    print("\n🛡️ تحليل الأمان:")
    cursor.execute('''
        SELECT 
            d.child_name,
            COUNT(CASE WHEN a.is_safe = 0 THEN 1 END) as unsafe_activities,
            COUNT(a.id) as total_activities
        FROM test_devices d
        LEFT JOIN test_activities a ON d.ip_address = a.device_ip
        GROUP BY d.child_name
    ''')
    
    safety_analysis = cursor.fetchall()
    for child_name, unsafe_count, total_count in safety_analysis:
        if total_count > 0:
            safety_percentage = ((total_count - unsafe_count) / total_count) * 100
            print(f"   👤 {child_name}: {safety_percentage:.1f}% أمان ({unsafe_count} من {total_count} يحتاج انتباه)")
    
    # إحصائيات الشبكة
    print(f"\n🌐 إحصائيات الشبكة:")
    cursor.execute('SELECT COUNT(*) FROM test_devices WHERE is_active = 1')
    active_devices = cursor.fetchone()[0]
    print(f"   • الأجهزة النشطة: {active_devices}")
    
    cursor.execute('SELECT COUNT(*) FROM test_activities WHERE DATE(timestamp) = DATE("now")')
    today_activities = cursor.fetchone()[0]
    print(f"   • أنشطة اليوم: {today_activities}")
    
    # التوصيات
    print("\n💡 التوصيات:")
    recommendations = generate_recommendations(children_added, activities, safety_analysis)
    for rec in recommendations:
        print(f"   {rec}")
    
    conn.close()
    print("\n🎉 تم إنجاز الاختبار بنجاح!")
    return True

def simulate_child_activities(child: Dict) -> List[Dict]:
    """محاكاة أنشطة الطفل"""
    activities = []
    child_name = child['name']
    device_ip = child['device_ip']
    
    # محاكاة استخدام التطبيقات
    if child_name == "أحمد":
        activities.extend([
            {
                'device_ip': device_ip,
                'type': 'تطبيق مفتوح',
                'details': 'Microsoft Edge - Khan Academy (تعليمي)',
                'safe': True
            },
            {
                'device_ip': device_ip,
                'type': 'بحث في الإنترنت',
                'details': 'math homework help',
                'safe': True
            },
            {
                'device_ip': device_ip,
                'type': 'موقع مزار',
                'details': 'khanacademy.org/math',
                'safe': True
            }
        ])
    elif child_name == "فاطمة":
        activities.extend([
            {
                'device_ip': device_ip,
                'type': 'تطبيق مفتوح',
                'details': 'PBS Kids Games (تعليمي)',
                'safe': True
            },
            {
                'device_ip': device_ip,
                'type': 'بحث في الإنترنت',
                'details': 'fun games for kids',
                'safe': True
            },
            {
                'device_ip': device_ip,
                'type': 'موقع مزار',
                'details': 'pbskids.org',
                'safe': True
            }
        ])
    elif child_name == "محمد":
        activities.extend([
            {
                'device_ip': device_ip,
                'type': 'تطبيق مفتوح',
                'details': 'Chrome - GitHub (برمجة)',
                'safe': True
            },
            {
                'device_ip': device_ip,
                'type': 'بحث في الإنترنت',
                'details': 'python tutorials',
                'safe': True
            },
            {
                'device_ip': device_ip,
                'type': 'موقع مزار',
                'details': 'stackoverflow.com',
                'safe': True
            }
        ])
    
    return activities

def generate_recommendations(children_count: int, activities: List, safety_analysis: List) -> List[str]:
    """إنتاج التوصيات"""
    recommendations = []
    
    if children_count == 0:
        recommendations.append("⚠️ لا توجد أطفال نشطين في المراقبة")
    else:
        recommendations.append(f"✅ يتم مراقبة {children_count} طفل بنجاح")
    
    # تحليل مستوى الأمان العام
    total_unsafe = sum(unsafe_count for _, unsafe_count, _ in safety_analysis)
    total_activities = sum(total_count for _, _, total_count in safety_analysis)
    
    if total_activities > 0:
        safety_rate = ((total_activities - total_unsafe) / total_activities) * 100
        if safety_rate >= 90:
            recommendations.append("🌟 ممتاز! معدل الأمان عالي جداً")
        elif safety_rate >= 75:
            recommendations.append("👍 جيد! معدل الأمان مقبول")
        else:
            recommendations.append("⚠️ يحتاج تحسين في معدل الأمان")
    
    # توصيات خاصة
    recommendations.extend([
        "💬 تحدث مع أطفالك حول الأمان الرقمي بانتظام",
        "🔍 راجع الأنشطة المشبوهة مع الأطفال",
        "📚 شجع على الأنشطة التعليمية",
        "🕐 حافظ على التوازن بين الشاشة والأنشطة الأخرى",
        "🤝 بناء الثقة أهم من المراقبة الصارمة"
    ])
    
    return recommendations

if __name__ == "__main__":
    test_advanced_monitoring()