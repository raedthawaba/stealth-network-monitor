#!/data/data/com.termux/files/usr/bin/bash
cat > monitoring_system.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
echo "🛡️ نظام المراقبة الشامل للأطفال - إعداد سريع"
echo "================================================"

# إنشاء مجلد
mkdir -p ~/monitoring/{reports,database}
cd ~/monitoring

# تثبيت الحزم
echo "📦 تثبيت الحزم..."
pkg update -y >/dev/null 2>&1
pkg install -y python sqlite3 >/dev/null 2>&1

echo "✅ تم الإعداد!"
echo ""
echo "🎯 لبدء المراقبة:"
echo "python3 monitor.py"
echo ""
echo "📈 لعرض التقارير:"
echo "python3 show_reports.py"
echo ""
echo "🛑 لإيقاف المراقبة:"
echo "./stop.sh"
EOF