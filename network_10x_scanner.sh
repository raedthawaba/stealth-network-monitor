#!/data/data/com.termux/files/usr/bin/bash
echo "🔍 الماسح الجديد لشبكة 10.0.x.x..."
echo "========================================="

echo "📍 الخطوة 1: التحقق من IP الخاص بك..."
MY_IP=$(ip route get 8.8.8.8 2>/dev/null | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' | head -1)
echo "🔍 IP الخاص بك: $MY_IP"

if [[ $MY_IP == 10.0.* ]]; then
    NETWORK_BASE=$(echo $MY_IP | cut -d'.' -f1-2)
    echo "🌐 نطاق الشبكة: $NETWORK_BASE.x.x"
else
    echo "⚠️ IP غير متوقع، سيتم استخدام 10.0.0.x"
    NETWORK_BASE="10.0.0"
fi

echo ""
echo "📍 الخطوة 2: البحث في نطاق 10.0.x.x..."
echo "========================================="

ACTIVE_DEVICES=()

echo "🔍 اختبار 10.0.0.x (الشبكة الافتراضية)..."
for ip in {1..50}; do
    target="10.0.0.$ip"
    if ping -c 1 -W 1 "$target" >/dev/null 2>&1; then
        echo "✅ $target - متصل"
        ACTIVE_DEVICES+=("$target")
    fi
done

echo ""
echo "🔍 اختبار 10.0.7.x (شبكتك الحالية)..."
for ip in {1..50}; do
    target="10.0.7.$ip"
    if ping -c 1 -W 1 "$target" >/dev/null 2>&1; then
        echo "✅ $target - متصل"
        ACTIVE_DEVICES+=("$target")
    fi
done

echo ""
echo "📊 النتائج الإجمالية:"
echo "عدد الأجهزة النشطة: ${#ACTIVE_DEVICES[@]}"
if [ ${#ACTIVE_DEVICES[@]} -gt 1 ]; then
    echo "🎯 الأجهزة المكتشفة:"
    for device in "${ACTIVE_DEVICES[@]}"; do
        echo "  • $device"
    done
    echo ""
    echo "✅ تم العثور على أجهزة! الآن يمكن إعداد نظام المراقبة الشامل"
    echo "📝 انسخ عناوين IP هذه وأخبرني بها"
else
    echo "⚠️ لا توجد أجهزة أخرى - تحقق من اتصال الأطفال"
    echo "💡 تأكد من أن أجهزة الأطفال:"
    echo "   • متصلة بنفس WiFi"
    echo "   • ليست في وضع airplane mode"
    echo "   • على نفس شبكة 10.0.x.x"
fi