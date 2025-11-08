#!/bin/bash

echo "🔧 ماسح Termux محسن - مع إصلاح الأخطاء"
echo "="*50

echo "📋 مرحلة 1: فهم مشكلة التوصيل"
echo ""

# فحص nmap
echo "🔍 فحص nmap..."
if command -v nmap &> /dev/null; then
    echo "✅ nmap متوفر"
    NMAP_VERSION=$(nmap --version 2>/dev/null | head -1 || echo "unknown")
    echo "📋 الإصدار: $NMAP_VERSION"
else
    echo "❌ nmap غير متوفر"
    echo "🔧 تثبيت: pkg install nmap"
    exit 1
fi

# فحص أدوات الشبكة
echo ""
echo "🔍 فحص أدوات الشبكة..."
for tool in ip ifconfig ping; do
    if command -v $tool &> /dev/null; then
        echo "✅ $tool متوفر"
    else
        echo "❌ $tool غير متوفر"
    fi
done

echo ""
echo "="*60
echo "🎯 مرحلة 2: فحص الشبكة المحسن"
echo "="*60

# طريقة 1: فحص النطاق الشائع
echo ""
echo "🔍 المحاولة 1: النطاق الشائع (192.168.1.0/24)"
echo "⏳ فحص سريع (60 ثانية)..."

nmap -sn 192.168.1.1-100 --max-rate=100 -T4 > scan_192.txt 2>&1 &
NMAP_PID=$!

# انتظار 30 ثانية ثم إظهار التقدم
for i in {1..6}; do
    sleep 5
    echo "   ⏳ جاري الفحص... ${i}/6 (30 ثانية)"
    if ! kill -0 $NMAP_PID 2>/dev/null; then
        break
    fi
done

# إيقاف nmap إذا لم ينته بعد
if kill -0 $NMAP_PID 2>/dev/null; then
    echo "   ⚠️ إيقاف الفحص لإظهار النتائج"
    kill $NMAP_PID 2>/dev/null
    wait $NMAP_PID 2>/dev/null
fi

# فحص طريقة ping يدوية
echo ""
echo "🔍 المحاولة 2: فحص ping يدوي سريع"
echo "⏳ فحص كل 5 عناوين IP..."

FOUND_DEVICES=""
for i in {1,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100}; do
    IP="192.168.1.${i}"
    echo -n "   📱 $IP "
    
    if ping -c 1 -W 2 $IP > /dev/null 2>&1; then
        echo "✅ متصل"
        FOUND_DEVICES="$FOUND_DEVICES $IP"
    else
        echo "❌ غير متصل"
    fi
done

# فحص أداة ip
echo ""
echo "🔍 المحاولة 3: فحص ip tables"
if command -v ip &> /dev/null; then
    echo "📋 قائمة الأجهزة من ip:"
    ip neigh show 2>/dev/null | grep -v "FAILED\|INCOMPLETE" | while read line; do
        echo "   📱 $line"
    done
fi

# فحص أداة arp
echo ""
echo "🔍 المحاولة 4: فحص arp table"
if command -v arp &> /dev/null; then
    echo "📋 arp table:"
    arp -a 2>/dev/null || arp 2>/dev/null | while read line; do
        echo "   📱 $line"
    done
fi

echo ""
echo "="*60
echo "📊 النتائج النهائية:"
echo "="*60

# عرض نتائج nmap
echo ""
echo "🔍 نتائج nmap (192.168.1.1-100):"
if [ -f scan_192.txt ]; then
    NMAP_COUNT=$(grep -c "Nmap scan report" scan_192.txt 2>/dev/null || echo "0")
    echo "📈 عدد الأجهزة من nmap: $NMAP_COUNT"
    
    if [ "$NMAP_COUNT" -gt "0" ]; then
        echo "📱 الأجهزة المكتشفة:"
        grep -E "Nmap scan report|Host is up" scan_192.txt | head -10
    fi
else
    echo "❌ لم يتم إنشاء ملف scan_192.txt"
fi

# عرض نتائج ping
echo ""
echo "🔍 نتائج ping المباشر:"
if [ ! -z "$FOUND_DEVICES" ]; then
    echo "📈 الأجهزة المتصلة (ping): $FOUND_DEVICES"
    echo "✅ تم العثور على أجهزة!"
    TOTAL_PING=$(echo $FOUND_DEVICES | wc -w)
    echo "📊 عدد الأجهزة: $TOTAL_PING"
else
    echo "❌ لم يتم العثور على أجهزة بالـ ping"
fi

# خاتمة
echo ""
echo "="*60
echo "📋 التقييم النهائي:"
echo "="*60

TOTAL_FOUND=$((NMAP_COUNT + TOTAL_PING))
if [ "$TOTAL_FOUND" -gt "0" ]; then
    echo "🎉 نجح الفحص! تم العثور على $TOTAL_FOUND جهاز"
    echo ""
    echo "✅ الخطوات التالية:"
    echo "1. احفظ عناوين IP التي ظهرت"
    echo "2. سنقوم بتحديث ملف التكوين"
    echo "3. سنبدأ مراقبة الأطفال"
    echo ""
    echo "📝 عناوين IP للتذكير:"
    if [ "$NMAP_COUNT" -gt "0" ]; then
        grep -oE '(\d+\.){3}\d+' scan_192.txt | head -5
    fi
    if [ ! -z "$FOUND_DEVICES" ]; then
        echo "$FOUND_DEVICES"
    fi
else
    echo "❌ لم يتم العثور على أجهزة"
    echo ""
    echo "💡 الحلول المقترحة:"
    echo "1. تأكد من اتصال الأطفال بالـ WiFi"
    echo "2. اطلب منهم فتح تطبيق على الهاتف"
    echo "3. تحقق من إعدادات الراوتر"
    echo "4. جرب الفحص في وقت آخر"
fi

echo "="*60