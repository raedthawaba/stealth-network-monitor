#!/bin/bash
# إعداد سريع لمراقبة DNS
# يعمل في Termux ويراقب كل النطاقات المزارة

echo "🚀 إعداد مراقبة DNS السريع..."
echo "====================================="

# تثبيت dnsmasq
echo "📦 تثبيت dnsmasq..."
pkg install dnsmasq -y

# إنشاء مجلد للسجلات
mkdir -p /data/data/com.termux/files/home/monitor_logs

# إنشاء ملف الإعدادات
cat > dnsmasq.conf << 'EOF'
# إعدادات مراقبة DNS للأطفال
log-queries
log-facility=/data/data/com.termux/files/home/monitor_logs/dns_queries.log
log-queries-extra

# استخدام خوادم DNS الخارجية
no-resolv
server=8.8.8.8
server=8.8.4.4

# تسجيل النطاقات المحظورة
log-failed
local-ttl=0
cache-size=1000
EOF

echo "✅ تم إنشاء ملف الإعدادات"

# بدء dnsmasq
echo "🚀 بدء مراقبة DNS..."
nohup dnsmasq -C dnsmasq.conf > /dev/null 2>&1 &
sleep 2

# فحص إذا كان يعمل
if pgrep -f "dnsmasq" > /dev/null; then
    echo "✅ تم بدء مراقبة DNS بنجاح!"
    echo "📄 السجلات في: /data/data/com.termux/files/home/monitor_logs/dns_queries.log"
    echo ""
    echo "🔍 لمراجعة آخر طلبات DNS:"
    echo "tail -f /data/data/com.termux/files/home/monitor_logs/dns_queries.log"
    echo ""
    echo "📊 لعرض المواقع الأكثر زيارة:"
    echo "grep -o 'query\\[[^]]*\\] [^ ]*' monitor_logs/dns_queries.log | sort | uniq -c | sort -nr | head -20"
else
    echo "❌ فشل في بدء dnsmasq"
    echo "📝 لعرض الأخطاء:"
    echo "cat dnsmasq.log"
fi

echo "====================================="