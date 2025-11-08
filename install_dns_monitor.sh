#!/bin/bash
# حل مراقبة DNS للأطفال
# يراقب كل النطاقات المزارة

# تثبيت dnsmasq للـ DNS logging
pkg install dnsmasq -y

# إنشاء ملف الإعدادات
cat > dnsmasq.conf << 'EOF'
# إعدادات مراقبة DNS
log-queries
log-facility=/data/data/com.termux/files/home/dns_queries.log
no-resolv
server=8.8.8.8
server=8.8.4.4
address=/#/8.8.8.8

# تسجيل النطاقات المشبوهة
log-queries-extra
EOF

# بدء dnsmasq
nohup dnsmasq -C dnsmasq.conf > /dev/null 2>&1 &

echo "✅ تم بدء مراقبة DNS"
echo "📄 السجلات محفوظة في: dns_queries.log"
echo "📊 لمراجعة آخر 50 طلب: tail -n 50 dns_queries.log"
