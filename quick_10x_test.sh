#!/data/data/com.termux/files/usr/bin/bash
echo "⚡ اختبار سريع لشبكة 10.0.x.x"
echo "========================================="

echo "📍 اختبار نطاق 10.0.0.x..."
echo "جاري فحص الأرقام الشائعة..."

ACTIVE_COUNT=0
for ip in 1 5 10 15 20 25 30 50 100 254; do
    target="10.0.0.$ip"
    if ping -c 1 -W 1 "$target" >/dev/null 2>&1; then
        echo "✅ $target - متصل"
        ACTIVE_COUNT=$((ACTIVE_COUNT + 1))
    fi
done

echo ""
echo "📍 اختبار نطاق 10.0.7.x..."
for ip in 1 5 10 15 20 25 30 50 100 254; do
    target="10.0.7.$ip"
    if ping -c 1 -W 1 "$target" >/dev/null 2>&1; then
        echo "✅ $target - متصل"
        ACTIVE_COUNT=$((ACTIVE_COUNT + 1))
    fi
done

echo ""
echo "📊 المجموع: $ACTIVE_COUNT جهاز نشط"
if [ $ACTIVE_COUNT -gt 1 ]; then
    echo "🎉 نجح! تم العثور على أجهزة متصلة"
else
    echo "⚠️ قد تكون المشكلة في اتصال الأطفال"
fi