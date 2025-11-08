#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 برنامج تجريبي لتشغيل نظام المراقبة الأبوية
تسجيل أنشطة وهمية للاختبار
"""

import json
import sqlite3
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict

class ParentalControlDemo:
    """نظام المراقبة التجريبي"""
    
    def __init__(self):
        self.db_path = "demo_parental_control.db"
        self.init_demo_database()
        self.load_children_config()
    
    def init_demo_database(self):
        """إنشاء قاعدة بيانات تجريبية"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # جدول الأطفال
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS children (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age_range TEXT,
                device_ip TEXT,
                device_type TEXT,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # جدول الأنشطة
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_name TEXT,
                device_ip TEXT,
                activity_type TEXT,
                activity_description TEXT,
                app_name TEXT,
                safety_level TEXT,
                risk_score REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول البحث
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                child_name TEXT,
                device_ip TEXT,
                search_engine TEXT,
                search_terms TEXT,
                search_url TEXT,
                is_inappropriate BOOLEAN,
                risk_level TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_children_config(self):
        """تحميل إعدادات الأطفال"""
        try:
            with open('parental_config.json', 'r', encoding='utf-8') as f:
                self.children = json.load(f).get('children', [])
        except:
            self.children = []
    
    def add_child(self, name: str, age: str, ip: str, device_type: str):
        """إضافة طفل جديد للمراقبة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO children 
            (name, age_range, device_ip, device_type, is_active)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, age, ip, device_type, True))
        
        conn.commit()
        conn.close()
        print(f"✅ تم إضافة الطفل: {name} ({age}) - {ip}")
    
    def log_activity(self, child_name: str, device_ip: str, activity_type: str, 
                    description: str, app_name: str = "", safety_level: str = "آمن", 
                    risk_score: float = 0.1):
        """تسجيل نشاط الطفل"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO activities 
            (child_name, device_ip, activity_type, activity_description, 
             app_name, safety_level, risk_score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (child_name, device_ip, activity_type, description, 
              app_name, safety_level, risk_score))
        
        conn.commit()
        conn.close()
    
    def log_search(self, child_name: str, device_ip: str, search_engine: str, 
                  search_terms: str, is_inappropriate: bool = False):
        """تسجيل عملية بحث"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        risk_level = "عالي" if is_inappropriate else "منخفض"
        
        search_url = f"https://{search_engine}/search?q={search_terms.replace(' ', '+')}"
        
        cursor.execute('''
            INSERT INTO search_activities 
            (child_name, device_ip, search_engine, search_terms, 
             search_url, is_inappropriate, risk_level)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (child_name, device_ip, search_engine, search_terms, 
              search_url, is_inappropriate, risk_level))
        
        conn.commit()
        conn.close()
    
    def generate_random_activities(self):
        """إنتاج أنشطة عشوائية للاختبار"""
        print("🎲 إنتاج أنشطة عشوائية للاختبار...")
        
        # أنشطة آمنة
        safe_activities = [
            ("Khan Academy - الرياضيات", "Microsoft Edge", "آمن", 0.1),
            ("PBS Kids Games", "Chrome", "آمن", 0.1),
            (" Scratch - البرمجة", "Firefox", "آمن", 0.1),
            ("YouTube - فيديوهات تعليمية", "Chrome", "آمن", 0.2),
            ("Wikipedia", "Safari", "آمن", 0.1)
        ]
        
        # أنشطة تحتاج انتباه
        moderate_activities = [
            ("Facebook", "Chrome", "يحتاج انتباه", 0.6),
            ("Instagram", "Safari", "يحتاج انتباه", 0.7),
            ("TikTok", "Chrome", "يحتاج انتباه", 0.8),
            ("Gaming Sites", "Firefox", "يحتاج انتباه", 0.5)
        ]
        
        # عمليات بحث آمنة
        safe_searches = [
            ("math homework", "Google", False),
            ("how to draw animals", "Bing", False),
            ("learn coding for kids", "Google", False),
            ("history of ancient Egypt", "Google", False)
        ]
        
        # عمليات بحث مشبوهة (للاختبار فقط)
        inappropriate_searches = [
            ("adult content", "Google", True),
            ("how to hack games", "Bing", True),
            ("free movie downloads", "Google", True)
        ]
        
        for child in self.children:
            child_name = child['name']
            device_ip = child['device_ip']
            
            # إضافة أنشطة آمنة
            for _ in range(random.randint(2, 4)):
                activity = random.choice(safe_activities)
                self.log_activity(child_name, device_ip, "تطبيق", 
                                f"استخدام {activity[0]}", activity[1], 
                                activity[2], activity[3])
            
            # إضافة أنشطة متوسطة
            for _ in range(random.randint(1, 2)):
                activity = random.choice(moderate_activities)
                self.log_activity(child_name, device_ip, "تطبيق", 
                                f"استخدام {activity[0]}", activity[1], 
                                activity[2], activity[3])
            
            # إضافة عمليات بحث
            for _ in range(random.randint(2, 3)):
                search = random.choice(safe_searches)
                self.log_search(child_name, device_ip, search[0], search[1], search[2])
            
            # إضافة عمليات بحث مشبوهة أحياناً
            if random.choice([True, False]):
                search = random.choice(inappropriate_searches)
                self.log_search(child_name, device_ip, search[0], search[1], search[2])
    
    def show_dashboard(self):
        """عرض لوحة التحكم"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        print("\n" + "="*60)
        print("🛡️ لوحة تحكم المراقبة الأبوية - وضع الاختبار")
        print("="*60)
        
        # عرض الأطفال
        cursor.execute("SELECT * FROM children WHERE is_active = 1")
        children = cursor.fetchall()
        
        print(f"\n👶 الأطفال المراقبون ({len(children)}):")
        for child in children:
            print(f"   • {child[1]} ({child[2]}) - {child[4]} - {child[3]}")
        
        # عرض الأنشطة الحديثة
        print(f"\n🔍 الأنشطة الحديثة:")
        cursor.execute('''
            SELECT child_name, activity_type, activity_description, 
                   app_name, safety_level, timestamp
            FROM activities 
            ORDER BY timestamp DESC 
            LIMIT 10
        ''')
        activities = cursor.fetchall()
        
        for activity in activities:
            child_name, act_type, desc, app, safety, timestamp = activity
            safety_icon = "✅" if safety == "آمن" else "⚠️"
            print(f"   {safety_icon} {child_name}: {act_type} - {desc}")
            if app:
                print(f"      💻 التطبيق: {app} ({timestamp[:19]})")
        
        # إحصائيات الأمان
        print(f"\n🛡️ إحصائيات الأمان:")
        cursor.execute('''
            SELECT safety_level, COUNT(*)
            FROM activities 
            GROUP BY safety_level
        ''')
        safety_stats = cursor.fetchall()
        
        for level, count in safety_stats:
            icon = "✅" if level == "آمن" else "⚠️"
            print(f"   {icon} {level}: {count} نشاط")
        
        # عمليات البحث المشبوهة
        print(f"\n🔍 عمليات البحث:")
        cursor.execute('''
            SELECT child_name, search_engine, search_terms, risk_level, timestamp
            FROM search_activities 
            ORDER BY timestamp DESC 
            LIMIT 5
        ''')
        searches = cursor.fetchall()
        
        for search in searches:
            child_name, engine, terms, risk, timestamp = search
            risk_icon = "🚨" if risk == "عالي" else "✅"
            print(f"   {risk_icon} {child_name}: {terms} ({engine}) - {risk}")
        
        conn.close()
    
    def generate_report(self):
        """إنشاء تقرير مفصل"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'children_count': 0,
            'total_activities': 0,
            'safety_summary': {},
            'top_apps': [],
            'alerts': []
        }
        
        # إحصائيات عامة
        cursor.execute("SELECT COUNT(*) FROM children WHERE is_active = 1")
        report['children_count'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM activities")
        report['total_activities'] = cursor.fetchone()[0]
        
        # ملخص الأمان
        cursor.execute('''
            SELECT safety_level, COUNT(*) 
            FROM activities 
            GROUP BY safety_level
        ''')
        report['safety_summary'] = dict(cursor.fetchall())
        
        # أهم التطبيقات
        cursor.execute('''
            SELECT app_name, COUNT(*) as usage_count
            FROM activities 
            WHERE app_name != ''
            GROUP BY app_name 
            ORDER BY usage_count DESC 
            LIMIT 5
        ''')
        report['top_apps'] = [dict(app_name=row[0], count=row[1]) for row in cursor.fetchall()]
        
        # التنبيهات
        cursor.execute('''
            SELECT child_name, activity_description, risk_score
            FROM activities 
            WHERE risk_score > 0.5
            ORDER BY risk_score DESC
        ''')
        alerts = []
        for row in cursor.fetchall():
            alerts.append({
                'child': row[0],
                'activity': row[1],
                'risk_level': 'عالي' if row[2] > 0.7 else 'متوسط'
            })
        report['alerts'] = alerts
        
        conn.close()
        
        return report
    
    def save_report(self):
        """حفظ التقرير في ملف"""
        report = self.generate_report()
        
        with open('demo_monitoring_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 تم حفظ التقرير في: demo_monitoring_report.json")

def main():
    """الدالة الرئيسية"""
    print("🎮 نظام المراقبة الأبوية - وضع الاختبار")
    print("=" * 50)
    
    demo = ParentalControlDemo()
    
    # إضافة الأطفال من ملف التكوين
    print("\n📋 تحميل الأطفال من ملف التكوين...")
    for child in demo.children:
        if child.get('is_active', False):
            demo.add_child(
                child['name'],
                child['age_range'],
                child['device_ip'],
                child['device_type']
            )
    
    # إنتاج أنشطة عشوائية
    demo.generate_random_activities()
    
    # عرض لوحة التحكم
    demo.show_dashboard()
    
    # حفظ التقرير
    demo.save_report()
    
    print(f"\n🎉 تم إنجاز الاختبار بنجاح!")
    print("💡 للاختبار مرة أخرى، قم بتشغيل: python demo_parental_control.py")

if __name__ == "__main__":
    main()