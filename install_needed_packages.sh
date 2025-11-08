#!/data/data/com.termux/files/usr/bin/bash
echo "🔧 تثبيت الحزم المطلوبة..."
pkg update -y
pkg install -y iproute2 nmap
echo "✅ تم تثبيت iproute2 و nmap بنجاح!"