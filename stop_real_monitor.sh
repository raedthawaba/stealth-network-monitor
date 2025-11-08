echo "🛑 إيقاف نظام المراقبة الحقيقية..."

# إيقاف جميع العمليات
pkill -f "real_monitor.py" 2>/dev/null || true
pkill -f "python3" 2>/dev/null || true

echo "✅ تم إيقاف النظام بنجاح!"

echo "📊 لمراجعة البيانات الحقيقية:"
echo "bash ~/real_monitoring/view_real_data.sh"
echo ""
echo "🔄 لإعادة التشغيل:"
echo "bash ~/real_monitoring/run_real_monitor.sh"