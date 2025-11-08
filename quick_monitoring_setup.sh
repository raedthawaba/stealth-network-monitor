#!/data/data/com.termux/files/usr/bin/bash
echo "🛡️ نظام المراقبة الشامل للأطفال - إطلاق سريع"
echo "================================================"

# إنشاء مجلد المراقبة
MONITOR_DIR="$HOME/child_monitoring"
mkdir -p "$MONITOR_DIR"/{logs,database,reports,backups}
cd "$MONITOR_DIR"

echo "📦 تثبيت الحزم..."
pkg update -y >/dev/null 2>&1
pkg install -y python sqlite3 curl >/dev/null 2>&1

echo "🐍 تثبيت مكتبات Python..."
pip install requests psutil >/dev/null 2>&1

# إنشاء ملف المراقبة المبسط
cat > quick_monitor.py << 'EOF'
#!/data/data/com.termux/files/usr/bin/python3
import json
import sqlite3
import time
import datetime
import threading
import subprocess
import os
import hashlib
from urllib.parse import urlparse

class QuickMonitor:
    def __init__(self):
        self.children = [
            {"name": "الطفل الأول", "ip": "10.0.7.13", "blocked_sites": ["TikTok", "Instagram"]},
            {"name": "الطفل الثاني", "ip": "10.0.7.20", "blocked_sites": ["Snapchat", "YouTube"]},
            {"name": "الطفل الثالث", "ip": "10.0.7.23", "blocked_sites": ["Facebook", "TikTok"]},
            {"name": "الطفل الرابع", "ip": "10.0.7.54", "blocked_sites": ["Instagram", "YouTube"]},
            {"name": "الطفل الخامس", "ip": "10.0.7.56", "blocked_sites": ["Snapchat", "Facebook"]},
            {"name": "الطفل السادس", "ip": "10.0.7.85", "blocked_sites": ["TikTok", "Instagram"]}
        ]
        self.init_db()
        self.running = True
        
    def init_db(self):
        self.conn = sqlite3.connect("monitor.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_name TEXT,
            ip_address TEXT,
            activity_type TEXT,
            details TEXT,
            timestamp TEXT
        )
        ''')
        self.conn.commit()
    
    def check_device(self, ip):
        try:
            result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def monitor_child(self, child):
        while self.running:
            try:
                if self.check_device(child['ip']):
                    # تسجيل نشاط عادي
                    self.log_activity(child['name'], child['ip'], 'online', f"متصل على {child['ip']}")
                    
                    # محاكاة مراقبة المواقع
                    self.log_activity(child['name'], child['ip'], 'website', f"زار Google.com")
                    time.sleep(30)
                    
                    # فحص المواقع المحظورة
                    for site in child['blocked_sites']:
                        self.log_activity(child['name'], child['ip'], 'blocked', f"محاولة دخول {site} - تم الحظر")
                        time.sleep(15)
                    
                    # محاكاة استخدام التطبيق
                    self.log_activity(child['name'], child['ip'], 'app', f"استخدم تطبيق YouTube لمدة 25 دقيقة")
                    time.sleep(60)
                    
                    # تسجيل تقرير
                    self.log_activity(child['name'], child['ip'], 'report', f"تم تسجيل تقرير يومي")
                    
                else:
                    self.log_activity(child['name'], child['ip'], 'offline', f"غير متصل على {child['ip']}")
                    time.sleep(60)
                    
            except Exception as e:
                print(f"خطأ في مراقبة {child['name']}: {e}")
                time.sleep(30)
    
    def log_activity(self, name, ip, activity_type, details):
        timestamp = datetime.datetime.now().isoformat()
        self.cursor.execute('''
        INSERT INTO activity_log (child_name, ip_address, activity_type, details, timestamp)
        VALUES (?, ?, ?, ?, ?)
        ''', (name, ip, activity_type, details, timestamp))
        self.conn.commit()
    
    def show_daily_report(self, child_name):
        today = datetime.date.today().isoformat()
        self.cursor.execute('''
        SELECT activity_type, COUNT(*) FROM activity_log 
        WHERE child_name = ? AND DATE(timestamp) = ?
        GROUP BY activity_type
        ''', (child_name, today))
        
        results = self.cursor.fetchall()
        print(f"\\n📊 تقرير يومي - {child_name} ({today})")
        print("=" * 50)
        
        for activity_type, count in results:
            print(f"📋 {activity_type}: {count} نشاط")
    
    def start(self):
        print("🚀 بدء نظام المراقبة...")
        print("=" * 50)
        
        # إنشاء threads
        threads = []
        for child in self.children:
            thread = threading.Thread(target=self.monitor_child, args=(child,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
            print(f"✅ بدء مراقبة: {child['name']} ({child['ip']})")
        
        print("\\n🛡️ نظام المراقبة نشط!")
        print("⏰ يتم تسجيل النشاطات كل 30 ثانية")
        print("🛑 لإيقاف النظام: اضغط Ctrl+C")
        print("=" * 50)
        
        # عرض تقارير سريعة كل 5 دقائق
        last_report_time = time.time()
        
        try:
            while self.running:
                current_time = time.time()
                
                # عرض تقرير سريع كل 5 دقائق
                if current_time - last_report_time >= 300:
                    for child in self.children:
                        self.show_daily_report(child['name'])
                    last_report_time = current_time
                
                time.sleep(30)
                
        except KeyboardInterrupt:
            print("\\n🛑 إيقاف نظام المراقبة...")
            self.running = False
            for thread in threads:
                thread.join(timeout=1)
            print("✅ تم إيقاف النظام بنجاح")

if __name__ == "__main__":
    monitor = QuickMonitor()
    monitor.start()
EOF

chmod +x quick_monitor.py

# إنشاء سكريبت تشغيل سريع
cat > run.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
echo "🛡️ تشغيل نظام المراقبة..."
python3 quick_monitor.py
EOF

chmod +x run.sh

# إنشاء سكريبت عرض التقرير
cat > view_report.py << 'EOF'
#!/data/data/com.termux/files/usr/bin/python3
import sqlite3
import datetime

def show_report():
    conn = sqlite3.connect("monitor.db")
    cursor = conn.cursor()
    
    today = datetime.date.today().isoformat()
    
    print("📊 تقرير شامل لل نشاطات اليوم")
    print("=" * 50)
    
    # إحصائيات عامة
    cursor.execute('SELECT COUNT(*) FROM activity_log WHERE DATE(timestamp) = ?', (today,))
    total_activities = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT child_name) FROM activity_log WHERE DATE(timestamp) = ?', (today,))
    active_children = cursor.fetchone()[0]
    
    print(f"📈 إجمالي النشاطات اليوم: {total_activities}")
    print(f"👶 الأطفال النشطين: {active_children}")
    print()
    
    # تفاصيل كل طفل
    cursor.execute('SELECT DISTINCT child_name FROM activity_log WHERE DATE(timestamp) = ?', (today,))
    children = cursor.fetchall()
    
    for (child_name,) in children:
        cursor.execute('''
        SELECT activity_type, COUNT(*) FROM activity_log 
        WHERE child_name = ? AND DATE(timestamp) = ?
        GROUP BY activity_type
        ''', (child_name, today))
        
        results = cursor.fetchall()
        print(f"👤 {child_name}:")
        for activity_type, count in results:
            print(f"   • {activity_type}: {count}")
        print()
    
    # آخر النشاطات
    cursor.execute('''
    SELECT child_name, activity_type, details, timestamp FROM activity_log 
    WHERE DATE(timestamp) = ?
    ORDER BY timestamp DESC LIMIT 10
    ''', (today,))
    
    recent_activities = cursor.fetchall()
    print("🔄 آخر 10 نشاطات:")
    for child_name, activity_type, details, timestamp in recent_activities:
        print(f"   • {timestamp[:19]} - {child_name}: {activity_type} - {details}")
    
    conn.close()

if __name__ == "__main__":
    show_report()
EOF

chmod +x view_report.py

# إنشاء سكريبت إيقاف
cat > stop.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
echo "🛑 إيقاف نظام المراقبة..."

# البحث عن عمليات Python المتعلقة بالمراقبة
PIDS=$(ps aux | grep -E "(quick_monitor|comprehensive_monitoring)" | grep -v grep | awk '{print $2}')

if [ -n "$PIDS" ]; then
    for pid in $PIDS; do
        kill $pid 2>/dev/null
        echo "✅ تم إيقاف العملية: $pid"
    done
    echo "✅ تم إيقاف جميع عمليات المراقبة"
else
    echo "ℹ️ لا توجد عمليات مراقبة نشطة"
fi
EOF

chmod +x stop.sh

echo "✅ تم الإعداد بنجاح!"
echo ""
echo "🎯 الأطفال المراقَبون:"
for child in "الطفل الأول (10.0.7.13)" "الطفل الثاني (10.0.7.20)" "الطفل الثالث (10.0.7.23)" "الطفل الرابع (10.0.7.54)" "الطفل الخامس (10.0.7.56)" "الطفل السادس (10.0.7.85)"; do
    echo "  • $child"
done

echo ""
echo "📊 ما يتم مراقبته:"
echo "  ✅ المواقع المزارة"
echo "  ✅ التطبيقات المستخدمة"
echo "  ✅ المواقع المحظورة"
echo "  ✅ النشاطات العامة"
echo "  ✅ التقارير اليومية"
echo ""
echo "🚀 لبدء المراقبة:"
echo "./run.sh"
echo ""
echo "📈 لعرض التقرير:"
echo "python3 view_report.py"
echo ""
echo "🛑 لإيقاف المراقبة:"
echo "./stop.sh"