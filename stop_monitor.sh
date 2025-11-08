echo "🛑 إيقاف نظام المراقبة الشامل..."

# إيقاف جميع العمليات المرتبطة بالمراقبة
pkill -f "universal_monitor.py" 2>/dev/null || true
pkill -f "python3" 2>/dev/null || true

# أو يمكن إيقاف العمليات المحددة
pkill -f "python3 universal_monitor.py" 2>/dev/null || true

echo "✅ تم إيقاف النظام بنجاح!"

echo "📊 لمراجعة التقارير:"
echo "bash ~/universal_monitoring/view_reports.sh"
echo ""
echo "🔄 لإعادة التشغيل:"
echo "bash ~/universal_monitoring/start_universal_monitor.sh"