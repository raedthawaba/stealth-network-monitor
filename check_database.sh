cd ~/monitoring

echo "📊 تقرير قاعدة بيانات المراقبة"
echo "=================================================="
echo ""

echo "🔍 آخر 10 أنشطة مسجلة:"
sqlite3 monitoring.db "SELECT child_name, activity_type, details, blocked, timestamp FROM activities ORDER BY timestamp DESC LIMIT 10"
echo ""

echo "📱 حالة الأجهزة الحديثة:"
sqlite3 monitoring.db "SELECT child_name, ip_address, status, last_seen FROM device_status ORDER BY last_seen DESC LIMIT 10"
echo ""

echo "📈 إحصائيات إجمالي الأطفال:"
sqlite3 monitoring.db "SELECT child_name, COUNT(*) as total_activities FROM activities GROUP BY child_name"
echo ""

echo "🚫 محاولات محظورة لكل طفل:"
sqlite3 monitoring.db "SELECT child_name, COUNT(*) as blocked_attempts FROM activities WHERE blocked = 1 GROUP BY child_name"