#!/bin/bash

echo "🔧 ماسح متقدم للـ Termux - مصلح المشاكل"
echo "="*50

echo "📋 اختبار الطرق المختلفة للعثور على IP..."

# اختبار 1: ip route
echo ""
echo "🔍 الطريقة 1: ip route"
if command -v ip &> /dev/null; then
    IP1=$(ip route get 1.1.1.1 2>/dev/null | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' | head -1)
    echo "   النتيجة: $IP1"
    if [ ! -z "$IP1" ] && [ "$IP1" != "192.168.1.100" ]; then
        echo "   ✅ IP صحيح!"
        CORRECT_IP="$IP1"
    else
        echo "   ⚠️ IP غير صحيح أو فارغ"
    fi
else
    echo "   ❌ ip command غير متوفر"
fi

# اختبار 2: ifconfig
echo ""
echo "🔍 الطريقة 2: ifconfig"
if command -v ifconfig &> /dev/null; then
    IP2=$(ifconfig 2>/dev/null | grep 'inet ' | grep -v '127.0.0.1' | head -1 | awk '{print $2}' | cut -d':' -f2)
    echo "   النتيجة: $IP2"
    if [ ! -z "$IP2" ] && [ "$IP2" != "192.168.1.100" ]; then
        echo "   ✅ IP صحيح!"
        CORRECT_IP="$IP2"
    else
        echo "   ⚠️ IP غير صحيح أو فارغ"
    fi
else
    echo "   ❌ ifconfig command غير متوفر"
fi

# استخدام IP صحيح إذا وُجد
if [ ! -z "$CORRECT_IP" ]; then
    echo ""
    echo "🎯 استخدام IP الصحيح: $CORRECT_IP"
    NETWORK_BASE=$(echo $CORRECT_IP | cut -d'.' -f1-3)
    echo "🔍 نطاق الشبكة: $NETWORK_BASE.0/24"
else
    echo ""
    echo "⚠️ استخدام النطاق الشائع: 192.168.1.0/24"
    NETWORK_BASE="192.168.1"
fi

echo ""
echo "⏳ فحص الشبكة... (سترة_duration)"

# فحص تقليدي
echo "🔍 الفحص التقليدي..."
nmap -sn ${NETWORK_BASE}.0/24 --max-rate=50 -T3 > traditional_scan.txt 2>&1

# فحص محدود
echo "🔍 الفحص المحدود (1-50)..."
nmap -sn ${NETWORK_BASE}.1-50 --max-rate=200 > limited_scan.txt 2>&1

# فحص مفصل
echo "🔍 الفحص المفصل للأجهزة المعروفة..."
for i in {1..20}; do
    IP="${NETWORK_BASE}.${i}"
    ping -c 1 -W 1 $IP > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "   📱 متصل: $IP"
    fi
done > ping_scan.txt 2>&1

echo ""
echo "="*65
echo "📊 مقارنة النتائج:"
echo "="*65

# عدد الأجهزة من nmap التقليدي
DEVICES1=$(grep -c "Nmap scan report" traditional_scan.txt 2>/dev/null || echo "0")
echo "📈 فحص nmap الكامل (0-255): $DEVICES1 أجهزة"

# عدد الأجهزة من nmap المحدود  
DEVICES2=$(grep -c "Nmap scan report" limited_scan.txt 2>/dev/null || echo "0")
echo "📈 فحص nmap المحدود (1-50): $DEVICES2 أجهزة"

# عدد الأجهزة من ping
DEVICES3=$(grep -c "متصل:" ping_scan.txt 2>/dev/null || echo "0")
echo "📈 فحص ping المباشر: $DEVICES3 أجهزة"

# إظهار النتائج التفصيلية
echo ""
echo "🔍 التفاصيل من nmap المحدود:"
if [ -f limited_scan.txt ]; then
    grep -E "Nmap scan report|Host is up" limited_scan.txt
fi

echo ""
echo "🔍 التفاصيل من ping:"
if [ -f ping_scan.txt ]; then
    cat ping_scan.txt
fi

echo ""
echo "="*65
echo "📋 خلاصة النتائج:"
echo "="*65

if [ "$DEVICES1" -gt "0" ] || [ "$DEVICES2" -gt "0" ] || [ "$DEVICES3" -gt "0" ]; then
    echo "🎉 تم العثور على أجهزة!"
    echo "📱_children كانوا متصلين بالفعل!"
    echo ""
    echo "✅ الخطوات التالية:"
    echo "1. احفظ عناوين IP التي ظهرت"
    echo "2. سنقوم بتحديث ملف التكوين"
    echo "3. سنبدأ مراقبة الأطفال"
    TOTAL_FOUND=$((DEVICES1 + DEVICES2 + DEVICES3))
    echo "📊 إجمالي الأجهزة المكتشفة: $TOTAL_FOUND"
else
    echo "❌ لم يتم العثور على أجهزة"
    echo ""
    echo "💡 الأسباب المحتملة:"
    echo "1. الأطفال في وضع عدم الاتصال"
    echo "2. WiFi مختلف أو Guest network"
    echo "3. مشكلة في الراوتر"
    echo "4. اتصال ضعيف"
    echo ""
    echo "🔧 الحلول:"
    echo "1. تأكد من اتصال الأطفال بالـ WiFi"
    echo "2. اطلب منهم فتح تطبيق على الهاتف"
    echo "3. جرب الفحص مرة أخرى"
    echo "4. تحقق من إعدادات الراوتر"
fi

echo "="*65
echo "💾 الملفات المحفوظة:"
echo "• traditional_scan.txt"
echo "• limited_scan.txt" 
echo "• ping_scan.txt"
echo "="*65