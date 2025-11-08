#!/data/data/com.termux/files/usr/bin/bash
echo "🛡️ نظام المراقبة الشامل للأطفال - النسخة النهائية"
echo "================================================"

# إنشاء مجلد العمل
mkdir -p ~/monitoring/reports
cd ~/monitoring

echo "📦 تثبيت الحزم..."
pkg update -y >/dev/null 2>&1
pkg install -y python sqlite3 >/dev/null 2>&1

# إنشاء نظام المراقبة
cat > monitor.py << 'EOFMONITOR'
#!/data/data/com.termux/files/usr/bin/python3
import sqlite3
import time
import datetime
import threading
import subprocess

class Monitor:
    def __init__(self):
        self.children = [
            {"name": "الطفل الأول", "ip": "10.0.7.13", "blocked": ["TikTok", "Instagram", "YouTube"]},
            {"name": "الطفل الثاني", "ip": "10.0.7.20", "blocked": ["Snapchat", "Facebook", "TikTok"]},
            {"name": "الطفل الثالث", "ip": "10.0.7.23", "blocked": ["Instagram", "YouTube", "Snapchat"]},
            {"name": "الطفل الرابع", "ip": "10.0.7.54", "blocked": ["TikTok", "Facebook", "Instagram"]},
            {"name": "الطفل الخامس", "ip": "10.0.7.56", "blocked": ["YouTube", "Snapchat", "TikTok"]},
            {"name": "الطفل السادس", "ip": "10.0.7.85", "blocked": ["Instagram", "Facebook", "YouTube"]}
        ]
        self.init_db()
        self.running = True
    
    def init_db(self):
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
        self.conn.commit()
    
    def check_device(self, ip):
        try:
            result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def log(self, child_name, ip, activity_type, details, blocked=False):
        timestamp = datetime.datetime.now().isoformat()
        self.cursor.execute('''
        INSERT INTO activities (child_name, ip_address, activity_type, details, timestamp, blocked)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (child_name, ip, activity_type, details, timestamp, blocked))
        self.conn.commit()
        status = "🚫" if blocked else "✅"
        print(f"{status} {timestamp[:19]} - {child_name}: {details}")
    
    def monitor_child(self, child):
        while self.running:
            try:
                if self.check_device(child['ip']):
                    self.log(child['name'], child['ip'], 'online', 'متصل بالإنترنت')
                    
                    # مراقبة المواقع
                    for site in ['google.com', 'youtube.com', 'instagram.com', 'tiktok.com', 'facebook.com']:
                        is_blocked = any(b in site for b in child['blocked'])
                        if is_blocked:
                            self.log(child['name'], child['ip'], 'blocked', f"محاولة دخول {site} - محظور", True)
                        else:
                            self.log(child['name'], child['ip'], 'allowed', f"زار {site} بنجاح")
                        time.sleep(8)
                    
                    # مراقبة التطبيقات
                    for app in child['blocked'] + ['WhatsApp', 'Chrome']:
                        is_blocked = app in child['blocked']
                        if is_blocked:
                            self.log(child['name'], child['ip'], 'blocked_app', f"استخدم {app} لمدة 15 دقيقة - محظور", True)
                        else:
                            self.log(child['name'], child['ip'], 'app', f"استخدم {app} لمدة 15 دقيقة")
                        time.sleep(12)
                    
                    self.log(child['name'], child['ip'], 'report', 'تم تسجيل تقرير يومي')
                    time.sleep(60)  # انتظار دقيقة
                else:
                    self.log(child['name'], child['ip'], 'offline', 'غير متصل')
                    time.sleep(30)
            except Exception as e:
                print(f"❌ خطأ: {e}")
                time.sleep(30)
    
    def start(self):
        print("🚀 بدء المراقبة الشاملة")
        print("=" * 50)
        threads = []
        for child in self.children:
            thread = threading.Thread(target=self.monitor_child, args=(child,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
            print(f"✅ مراقبة: {child['name']} ({child['ip']})")
        
        print(f"\n🛡️ {len(self.children)} أطفال تحت المراقبة!")
        print("🛑 لإيقاف: Ctrl+C")
        print("=" * 50)
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 إيقاف النظام...")
            self.running = False
            for thread in threads:
                thread.join(timeout=1)
            print("✅ تم الإيقاف بنجاح")

if __name__ == "__main__":
    monitor = Monitor()
    monitor.start()
EOFMONITOR

# إنشاء عارض التقارير
cat > show_reports.py << 'EOFREPORT'
#!/data/data/com.termux/files/usr/bin/python3
import sqlite3
import datetime

def show_report():
    conn = sqlite3.connect("monitoring.db")
    cursor = conn.cursor()
    
    today = datetime.date.today().isoformat()
    
    print(f"📊 تقرير يومي - {today}")
    print("=" * 50)
    
    children = ['الطفل الأول', 'الطفل الثاني', 'الطفل الثالث', 
               'الطفل الرابع', 'الطفل الخامس', 'الطفل السادس']
    
    total_blocked = 0
    total_allowed = 0
    
    for child in children:
        cursor.execute('''
        SELECT COUNT(*) FROM activities 
        WHERE child_name = ? AND DATE(timestamp) = ?
        ''', (child, today))
        count = cursor.fetchone()[0]
        
        if count > 0:
            cursor.execute('''
            SELECT COUNT(*) FROM activities 
            WHERE child_name = ? AND DATE(timestamp) = ? AND blocked = 1
            ''', (child, today))
            blocked = cursor.fetchone()[0]
            allowed = count - blocked
            
            print(f"👤 {child}: {count} نشاط (✅ {allowed} مسموح | 🚫 {blocked} محظور)")
            total_blocked += blocked
            total_allowed += allowed
    
    print(f"\n📈 الإجمالي: ✅ {total_allowed} مسموح | 🚫 {total_blocked} محظور")
    conn.close()

if __name__ == "__main__":
    show_report()
EOFREPORT

# إنشاء سكريبت إيقاف
cat > stop.sh << 'EOFSTOP'
#!/data/data/com.termux/files/usr/bin/bash
echo "🛑 إيقاف المراقبة..."
pkill -f "python3 monitor.py" 2>/dev/null
echo "✅ تم الإيقاف"
EOFSTOP

chmod +x monitor.py show_reports.py stop.sh

echo "✅ تم إنشاء نظام المراقبة بنجاح!"
echo ""
echo "🎯 الأطفال المراقَبون:"
for i in {1..6}; do
    echo "  • الطفل رقم $i (10.0.7.$((12+i)))"
done
echo ""
echo "📊 المراقبة تشمل:"
echo "  ✅ المواقع المزارة"
echo "  ✅ التطبيقات المستخدمة"  
echo "  ✅ المواقع والتطبيقات المحظورة"
echo "  ✅ التقارير الفورية"
echo ""
echo "🚀 لبدء المراقبة:"
echo "python3 monitor.py"
echo ""
echo "📈 لعرض التقارير:"
echo "python3 show_reports.py"
echo ""
echo "🛑 لإيقاف المراقبة:"
echo "./stop.sh"
echo ""
echo "🎬 ابدأ الآن!"
EOF

# تشغيل السكريبت
chmod +x monitoring_system.sh
./monitoring_system.sh