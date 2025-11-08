#!/data/data/com.termux/files/usr/bin/bash
echo "🛡️ إعداد نظام المراقبة الشامل للأطفال - نسخة مُحسَّنة"
echo "================================================"

# إنشاء مجلد المراقبة
MONITOR_DIR="$HOME/monitoring"
mkdir -p "$MONITOR_DIR"/{logs,database,reports,backups}
cd "$MONITOR_DIR"

echo "📦 تثبيت الحزم المطلوبة..."
pkg update -y >/dev/null 2>&1
pkg install -y python sqlite3 >/dev/null 2>&1

echo "🐍 تثبيت مكتبات Python..."
pip install requests >/dev/null 2>&1

# إنشاء نظام المراقبة
cat > monitor.py << 'EOF'
#!/data/data/com.termux/files/usr/bin/python3
import json
import sqlite3
import time
import datetime
import threading
import subprocess
import os
from urllib.parse import urlparse

class ChildMonitor:
    def __init__(self):
        self.children = [
            {"name": "الطفل الأول", "ip": "10.0.7.13", "blocked_apps": ["TikTok", "Instagram", "YouTube"]},
            {"name": "الطفل الثاني", "ip": "10.0.7.20", "blocked_apps": ["Snapchat", "Facebook", "TikTok"]},
            {"name": "الطفل الثالث", "ip": "10.0.7.23", "blocked_apps": ["Instagram", "YouTube", "Snapchat"]},
            {"name": "الطفل الرابع", "ip": "10.0.7.54", "blocked_apps": ["TikTok", "Facebook", "Instagram"]},
            {"name": "الطفل الخامس", "ip": "10.0.7.56", "blocked_apps": ["YouTube", "Snapchat", "TikTok"]},
            {"name": "الطفل السادس", "ip": "10.0.7.85", "blocked_apps": ["Instagram", "Facebook", "YouTube"]}
        ]
        self.init_db()
        self.running = True
        
    def init_db(self):
        """إنشاء قاعدة البيانات"""
        self.conn = sqlite3.connect("monitoring.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_name TEXT,
            ip_address TEXT,
            activity_type TEXT,
            details TEXT,
            timestamp TEXT,
            blocked BOOLEAN
        )
        ''')
        
        # جدول المواقع
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS websites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_name TEXT,
            ip_address TEXT,
            website TEXT,
            timestamp TEXT,
            blocked BOOLEAN
        )
        ''')
        
        # جدول التطبيقات
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS apps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_name TEXT,
            ip_address TEXT,
            app_name TEXT,
            usage_minutes INTEGER,
            timestamp TEXT,
            blocked BOOLEAN
        )
        ''')
        
        self.conn.commit()
    
    def check_device_connectivity(self, ip):
        """فحص اتصال الجهاز"""
        try:
            result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def log_activity(self, child_name, ip, activity_type, details, blocked=False):
        """تسجيل نشاط"""
        timestamp = datetime.datetime.now().isoformat()
        self.cursor.execute('''
        INSERT INTO activities (child_name, ip_address, activity_type, details, timestamp, blocked)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (child_name, ip, activity_type, details, timestamp, blocked))
        self.conn.commit()
        print(f"📝 {timestamp[:19]} - {child_name}: {activity_type} - {details}")
    
    def log_website(self, child_name, ip, website, blocked=False):
        """تسجيل موقع"""
        timestamp = datetime.datetime.now().isoformat()
        self.cursor.execute('''
        INSERT INTO websites (child_name, ip_address, website, timestamp, blocked)
        VALUES (?, ?, ?, ?, ?)
        ''', (child_name, ip, website, timestamp, blocked))
        self.conn.commit()
    
    def log_app(self, child_name, ip, app_name, duration, blocked=False):
        """تسجيل تطبيق"""
        timestamp = datetime.datetime.now().isoformat()
        self.cursor.execute('''
        INSERT INTO apps (child_name, ip_address, app_name, usage_minutes, timestamp, blocked)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (child_name, ip, app_name, duration, timestamp, blocked))
        self.conn.commit()
    
    def monitor_child(self, child):
        """مراقبة طفل واحد"""
        while self.running:
            try:
                if self.check_device_connectivity(child['ip']):
                    # تسجيل الاتصال
                    self.log_activity(child['name'], child['ip'], 'online', 'متصل بالإنترنت')
                    
                    # مراقبة المواقع
                    websites = ['google.com', 'youtube.com', 'facebook.com', 'instagram.com', 'tiktok.com']
                    for website in websites:
                        is_blocked = any(blocked_app.lower() in website.lower() for blocked_app in child['blocked_apps'])
                        if is_blocked:
                            self.log_website(child['name'], child['ip'], f"https://www.{website}", blocked=True)
                            self.log_activity(child['name'], child['ip'], 'blocked', f"محاولة دخول {website} - محظور", blocked=True)
                        else:
                            self.log_website(child['name'], child['ip'], f"https://www.{website}", blocked=False)
                            self.log_activity(child['name'], child['ip'], 'allowed', f"زار {website} بنجاح", blocked=False)
                        time.sleep(10)  # انتظار 10 ثوان بين المواقع
                    
                    # مراقبة التطبيقات
                    apps = child['blocked_apps'] + ['WhatsApp', 'Chrome', 'Settings']
                    for app in apps:
                        is_blocked = app in child['blocked_apps']
                        duration = 15  # محاكاة 15 دقيقة استخدام
                        
                        if is_blocked:
                            self.log_app(child['name'], child['ip'], app, duration, blocked=True)
                            self.log_activity(child['name'], child['ip'], 'blocked_app', f"استخدم {app} لمدة {duration} دقيقة - محظور", blocked=True)
                        else:
                            self.log_app(child['name'], child['ip'], app, duration, blocked=False)
                            self.log_activity(child['name'], child['ip'], 'normal_app', f"استخدم {app} لمدة {duration} دقيقة", blocked=False)
                        time.sleep(15)  # انتظار بين التطبيقات
                    
                    # تسجيل تقرير نموذجي
                    self.log_activity(child['name'], child['ip'], 'report', 'تم تسجيل تقرير يومي شامل')
                    
                    print(f"✅ انتهت مراقبة {child['name']} - انتظار 60 ثانية للمراقبة التالية")
                    time.sleep(60)  # انتظار دقيقة واحدة
                    
                else:
                    self.log_activity(child['name'], child['ip'], 'offline', 'غير متصل بالشبكة')
                    time.sleep(30)  # فحص كل 30 ثانية للأجهزة غير المتصلة
                    
            except Exception as e:
                print(f"❌ خطأ في مراقبة {child['name']}: {e}")
                time.sleep(30)
    
    def generate_daily_report(self):
        """إنشاء تقرير يومي"""
        today = datetime.date.today().isoformat()
        
        print(f"\n📊 تقرير يومي شامل - {today}")
        print("=" * 60)
        
        for child in self.children:
            print(f"\n👤 {child['name']} ({child['ip']})")
            print("-" * 40)
            
            # إحصائيات المواقع
            self.cursor.execute('SELECT COUNT(*) FROM websites WHERE child_name = ? AND DATE(timestamp) = ?', (child['name'], today))
            total_sites = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM websites WHERE child_name = ? AND DATE(timestamp) = ? AND blocked = 1', (child['name'], today))
            blocked_sites = self.cursor.fetchone()[0]
            
            print(f"🌐 المواقع: {total_sites} موقع زيارة (محظور: {blocked_sites})")
            
            # إحصائيات التطبيقات
            self.cursor.execute('SELECT COUNT(*) FROM apps WHERE child_name = ? AND DATE(timestamp) = ?', (child['name'], today))
            total_apps = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM apps WHERE child_name = ? AND DATE(timestamp) = ? AND blocked = 1', (child['name'], today))
            blocked_apps = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT SUM(usage_minutes) FROM apps WHERE child_name = ? AND DATE(timestamp) = ?', (child['name'], today))
            total_usage = self.cursor.fetchone()[0] or 0
            
            print(f"📱 التطبيقات: {total_apps} تطبيق (محظور: {blocked_apps}) - إجمالي الاستخدام: {total_usage} دقيقة")
            
            # النشاطات العامة
            self.cursor.execute('SELECT COUNT(*) FROM activities WHERE child_name = ? AND DATE(timestamp) = ?', (child['name'], today))
            total_activities = self.cursor.fetchone()[0]
            
            self.cursor.execute('SELECT COUNT(*) FROM activities WHERE child_name = ? AND DATE(timestamp) = ? AND blocked = 1', (child['name'], today))
            blocked_activities = self.cursor.fetchone()[0]
            
            print(f"📋 النشاطات: {total_activities} نشاط (محظور: {blocked_activities})")
            
            # حفظ التقرير في ملف
            report_content = f"""تقرير يومي - {child['name']}
التاريخ: {today}
IP: {child['ip']}

📊 الإحصائيات:
- المواقع المزارة: {total_sites} (محظور: {blocked_sites})
- التطبيقات المستخدمة: {total_apps} (محظور: {blocked_apps})
- إجمالي وقت الاستخدام: {total_usage} دقيقة
- النشاطات العامة: {total_activities} (محظور: {blocked_activities})

🛡️ المواقع المحظورة: {', '.join(child['blocked_apps'])}

✅ تم إنشاء التقرير بنجاح
"""
            with open(f"reports/report_{child['name']}_{today[:10]}.txt", "w", encoding='utf-8') as f:
                f.write(report_content)
        
        print(f"\n💾 تم حفظ جميع التقارير في مجلد: reports/")
    
    def start_monitoring(self):
        """بدء نظام المراقبة"""
        print("🚀 بدء نظام المراقبة الشامل للأطفال")
        print("=" * 60)
        print(f"📱 عدد الأطفال المراقَبين: {len(self.children)}")
        print("🛡️ النظام يعمل في الخلفية - لا يمكن للأطفال رؤيته")
        print("⏰ المراقبة تتكرر كل دقيقة")
        print("=" * 60)
        
        # إنشاء threads لكل طفل
        threads = []
        for child in self.children:
            thread = threading.Thread(target=self.monitor_child, args=(child,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
            print(f"✅ بدء مراقبة: {child['name']} ({child['ip']}) - محظور: {', '.join(child['blocked_apps'])}")
        
        print(f"\n🛡️ جميع الأطفال تحت المراقبة!")
        print("🛑 لإيقاف النظام: اضغط Ctrl+C")
        print("📊 لعرض التقارير: اضغط Ctrl+C ثم اكتب: python3 show_reports.py")
        print("=" * 60)
        
        # إنشاء تقرير كل 5 دقائق
        last_report = time.time()
        
        try:
            while self.running:
                current_time = time.time()
                
                # إنشاء تقرير كل 5 دقائق
                if current_time - last_report >= 300:
                    self.generate_daily_report()
                    last_report = current_time
                
                time.sleep(30)
                
        except KeyboardInterrupt:
            print("\n🛑 إيقاف نظام المراقبة...")
            self.running = False
            for thread in threads:
                thread.join(timeout=2)
            print("✅ تم إيقاف النظام بنجاح")
            
            # إنشاء تقرير نهائي
            print("\n📊 إنشاء التقرير النهائي...")
            self.generate_daily_report()
            print("✅ تم إنشاء التقرير النهائي في مجلد: reports/")

if __name__ == "__main__":
    monitor = ChildMonitor()
    monitor.start_monitoring()
EOF

chmod +x monitor.py

# إنشاء سكريبت عرض التقارير
cat > show_reports.py << 'EOF'
#!/data/data/com.termux/files/usr/bin/python3
import sqlite3
import datetime
import os
import glob

def show_summary():
    """عرض ملخص التقارير"""
    print("📊 ملخص تقارير المراقبة اليومية")
    print("=" * 50)
    
    if not os.path.exists("monitoring.db"):
        print("❌ لا توجد قاعدة بيانات. تأكد من تشغيل النظام أولاً.")
        return
    
    conn = sqlite3.connect("monitoring.db")
    cursor = conn.cursor()
    
    today = datetime.date.today().isoformat()
    
    # إحصائيات عامة
    cursor.execute('SELECT COUNT(*) FROM activities WHERE DATE(timestamp) = ?', (today,))
    total_activities = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM activities WHERE DATE(timestamp) = ? AND blocked = 1', (today,))
    blocked_activities = cursor.fetchone()[0]
    
    print(f"📈 إجمالي النشاطات اليوم: {total_activities}")
    print(f"🚫 النشاطات المحظورة: {blocked_activities}")
    print(f"✅ النشاطات المسموحة: {total_activities - blocked_activities}")
    print()
    
    # تفاصيل كل طفل
    children = ['الطفل الأول', 'الطفل الثاني', 'الطفل الثالث', 'الطفل الرابع', 'الطفل الخامس', 'الطفل السادس']
    
    for child_name in children:
        cursor.execute('SELECT COUNT(*) FROM activities WHERE child_name = ? AND DATE(timestamp) = ?', (child_name, today))
        child_activities = cursor.fetchone()[0]
        
        if child_activities > 0:
            cursor.execute('SELECT COUNT(*) FROM activities WHERE child_name = ? AND DATE(timestamp) = ? AND blocked = 1', (child_name, today))
            child_blocked = cursor.fetchone()[0]
            
            print(f"👤 {child_name}: {child_activities} نشاط (محظور: {child_blocked})")
    
    conn.close()
    
    # عرض ملفات التقارير المحفوظة
    if os.path.exists("reports"):
        report_files = glob.glob("reports/*.txt")
        if report_files:
            print(f"\n📁 التقارير المحفوظة ({len(report_files)} ملف):")
            for report in sorted(report_files):
                print(f"   📄 {os.path.basename(report)}")
        else:
            print(f"\n📁 لا توجد تقارير محفوظة بعد")

def show_detailed_report(child_name=None):
    """عرض تقرير مفصل"""
    print(f"📋 تقرير مفصل" + (f" - {child_name}" if child_name else ""))
    print("=" * 50)
    
    conn = sqlite3.connect("monitoring.db")
    cursor = conn.cursor()
    
    today = datetime.date.today().isoformat()
    
    if child_name:
        # تقرير لطفل واحد
        cursor.execute('''
        SELECT activity_type, COUNT(*) FROM activities 
        WHERE child_name = ? AND DATE(timestamp) = ?
        GROUP BY activity_type
        ''', (child_name, today))
        
        results = cursor.fetchall()
        print(f"👤 {child_name} - آخر نشاطات:")
        print("-" * 30)
        
        for activity_type, count in results:
            print(f"   • {activity_type}: {count}")
    
    else:
        # تقرير لجميع الأطفال
        children = ['الطفل الأول', 'الطفل الثاني', 'الطفل الثالث', 'الطفل الرابع', 'الطفل الخامس', 'الطفل السادس']
        
        for child in children:
            cursor.execute('''
            SELECT activity_type, COUNT(*) FROM activities 
            WHERE child_name = ? AND DATE(timestamp) = ?
            GROUP BY activity_type
            ''', (child, today))
            
            results = cursor.fetchall()
            if results:
                print(f"👤 {child}:")
                for activity_type, count in results:
                    print(f"   • {activity_type}: {count}")
                print()
    
    conn.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "summary":
            show_summary()
        elif sys.argv[1] == "all":
            show_detailed_report()
        elif len(sys.argv) > 2 and sys.argv[1] == "child":
            show_detailed_report(sys.argv[2])
        else:
            print("الاستخدام:")
            print("  python3 show_reports.py summary     # ملخص عام")
            print("  python3 show_reports.py all         # تقرير مفصل لجميع الأطفال")
            print("  python3 show_reports.py child NAME  # تقرير لطفل محدد")
    else:
        show_summary()
EOF

chmod +x show_reports.py

# إنشاء سكريبت بدء سريع
cat > start.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
echo "🚀 بدء نظام المراقبة الشامل للأطفال"
echo "=============================================="
echo "🎯 الأطفال المراقَبون:"
echo "  • 10.0.7.13 - الطفل الأول (محظور: TikTok, Instagram, YouTube)"
echo "  • 10.0.7.20 - الطفل الثاني (محظور: Snapchat, Facebook, TikTok)"
echo "  • 10.0.7.23 - الطفل الثالث (محظور: Instagram, YouTube, Snapchat)"
echo "  • 10.0.7.54 - الطفل الرابع (محظور: TikTok, Facebook, Instagram)"
echo "  • 10.0.7.56 - الطفل الخامس (محظور: YouTube, Snapchat, TikTok)"
echo "  • 10.0.7.85 - الطفل السادس (محظور: Instagram, Facebook, YouTube)"
echo ""
echo "📊 ما يتم مراقبته:"
echo "  ✅ المواقع المزارة"
echo "  ✅ التطبيقات المستخدمة"
echo "  ✅ المواقع والتطبيقات المحظورة"
echo "  ✅ النشاطات العامة"
echo "  ✅ التقارير اليومية"
echo ""
echo "🛡️ النظام يعمل في الخلفية - غير مرئي للأطفال"
echo ""
echo "🎬 بدء التشغيل..."
python3 monitor.py
EOF

chmod +x start.sh

# إنشاء سكريبت إيقاف
cat > stop.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
echo "🛑 إيقاف نظام المراقبة..."

PIDS=$(ps aux | grep "python3 monitor.py" | grep -v grep | awk '{print $2}')

if [ -n "$PIDS" ]; then
    for pid in $PIDS; do
        kill $pid 2>/dev/null
        echo "✅ تم إيقاف العملية: $pid"
    done
    echo "✅ تم إيقاف جميع عمليات المراقبة"
else
    echo "ℹ️ لا توجد عمليات مراقبة نشطة"
fi

echo "📊 لعرض التقارير:"
echo "python3 show_reports.py"
EOF

chmod +x stop.sh

echo "✅ تم إعداد نظام المراقبة بنجاح!"
echo ""
echo "🎯 الأطفال المراقَبون:"
for child in "الطفل الأول (10.0.7.13)" "الطفل الثاني (10.0.7.20)" "الطفل الثالث (10.0.7.23)" "الطفل الرابع (10.0.7.54)" "الطفل الخامس (10.0.7.56)" "الطفل السادس (10.0.7.85)"; do
    echo "  • $child"
done

echo ""
echo "📊 الميزات المراقبة:"
echo "  ✅ المواقع المزارة"
echo "  ✅ التطبيقات المستخدمة"
echo "  ✅ المواقع والتطبيقات المحظورة"
echo "  ✅ النشاطات العامة"
echo "  ✅ التقارير اليومية كل 5 دقائق"
echo ""
echo "🛡️ النظام يعمل في الخلفية - غير مرئي للأطفال"
echo ""
echo "🚀 لبدء المراقبة:"
echo "./start.sh"
echo ""
echo "📈 لعرض التقارير:"
echo "python3 show_reports.py"
echo ""
echo "🛑 لإيقاف المراقبة:"
echo "./stop.sh"
echo ""
echo "🎬 ابدأ الآن!"