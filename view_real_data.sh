cd ~/real_monitoring

echo "📊 تقرير البيانات الحقيقية للمراقبة"
echo "=================================================="
echo ""

echo "🔍 جميع الأجهزة المكتشفة:"
sqlite3 real_monitoring.db "SELECT ip_address, mac_address, last_seen, total_connections FROM devices ORDER BY last_seen DESC"
echo ""

echo "🌐 الاتصالات الحقيقية الأخيرة:"
sqlite3 real_monitoring.db "SELECT device_ip, application_name, website_domain, dest_port, connection_start FROM real_connections ORDER BY connection_start DESC LIMIT 15"
echo ""

echo "📱 المواقع المزارة فعلياً:"
sqlite3 real_monitoring.db "SELECT device_ip, domain_name, visit_time, page_views FROM website_visits ORDER BY visit_time DESC LIMIT 10"
echo ""

echo "💻 التطبيقات المستخدمة:"
sqlite3 real_monitoring.db "SELECT device_ip, app_name, start_time FROM app_usage WHERE end_time IS NULL ORDER BY start_time DESC"
echo ""

echo "📊 إحصائيات حسب الجهاز:"
sqlite3 real_monitoring.db "SELECT device_ip, COUNT(*) as total_connections FROM real_connections GROUP BY device_ip ORDER BY total_connections DESC"
echo ""

echo "🔍 للاتصال والتفاصيل:"
echo "• الاتصالات: sqlite3 real_monitoring.db 'SELECT * FROM real_connections WHERE device_ip=\"10.0.7.20\"'"
echo "• المواقع: sqlite3 real_monitoring.db 'SELECT * FROM website_visits WHERE device_ip=\"10.0.7.13\"'"
echo "• التطبيقات: sqlite3 real_monitoring.db 'SELECT * FROM app_usage WHERE device_ip=\"10.0.7.23\"'"