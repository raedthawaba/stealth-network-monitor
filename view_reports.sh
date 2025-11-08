cd ~/universal_monitoring

echo "📊 تقرير المراقبة الشاملة للأجهزة"
echo "=================================================="
echo ""

echo "🔍 جميع الأجهزة المكتشفة:"
sqlite3 universal_monitoring.db "SELECT ip_address, last_seen, total_sessions FROM devices ORDER BY last_seen DESC"
echo ""

echo "📱 آخر 20 نشاط مسجل:"
sqlite3 universal_monitoring.db "SELECT device_ip, activity_type, details, category, risk_level, timestamp FROM detailed_activities ORDER BY timestamp DESC LIMIT 20"
echo ""

echo "📈 الأنشطة حسب الجهاز:"
sqlite3 universal_monitoring.db "SELECT device_ip, COUNT(*) as total_activities FROM detailed_activities GROUP BY device_ip ORDER BY total_activities DESC"
echo ""

echo "🚨 المواقع عالية المخاطر:"
sqlite3 universal_monitoring.db "SELECT destination, category, risk_level, COUNT(*) as visits FROM detailed_activities WHERE risk_level >= 4 GROUP BY destination ORDER BY visits DESC"
echo ""

echo "📊 تصنيف الأنشطة:"
sqlite3 universal_monitoring.db "SELECT category, COUNT(*) as count FROM detailed_activities GROUP BY category ORDER BY count DESC"
echo ""

echo "🔍 تفاصيل جهاز محدد (ادخل IP):"
echo "مثال: SELECT * FROM detailed_activities WHERE device_ip='10.0.7.20' ORDER BY timestamp DESC LIMIT 10"
echo "أو: sqlite3 universal_monitoring.db 'SELECT * FROM detailed_activities WHERE device_ip=\"10.0.7.20\" ORDER BY timestamp DESC LIMIT 10'"