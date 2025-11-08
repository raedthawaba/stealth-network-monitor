#!/bin/bash

echo "🌐 ماسح الشبكة للعثور على الأطفال الحقيقيين - إصدار Termux"
echo "="*55

# الحصول على عنوان IP في Termux
echo "🔍 جاري العثور على عنوان IP الخاص بك..."

# طريقة 1: استخدام ip route
if command -v ip &> /dev/null; then
    LOCAL_IP=$(ip route get 1.1.1.1 2>/dev/null | grep -oP 'src \K[\d.]+')
    if [ -z "$LOCAL_IP" ]; then
        # طريقة 2: استخدام ifconfig
        if command -v ifconfig &> /dev/null; then
            LOCAL_IP=$(ifconfig | grep 'inet ' | grep -v '127.0.0.1' | head -1 | awk '{print $2}' | cut -d':' -f2)
        else
            # طريقة 3: واجهة افتراضية
            LOCAL_IP="192.168.1.100"
        fi
    fi
else
    # طريقة 2: استخدام ifconfig
    if command -v ifconfig &> /dev/null; then
        LOCAL_IP=$(ifconfig | grep 'inet ' | grep -v '127.0.0.1' | head -1 | awk '{print $2}' | cut -d':' -f2)
    else
        # طريقة 3: واجهة افتراضية
        LOCAL_IP="192.168.1.100"
    fi
fi

echo "📍 عنوان IP الخاص بك: $LOCAL_IP"

# تحديد نطاق الشبكة
if [ ! -z "$LOCAL_IP" ]; then
    NETWORK_BASE=$(echo $LOCAL_IP | cut -d'.' -f1-3)
    echo "🔍 نطاق الشبكة: $NETWORK_BASE.0/24"
    
    echo ""
    echo "⏳ فحص الأجهزة المتصلة... (قد يستغرق 2-3 دقائق)"
    echo "🔎 باستخدام nmap..."
    
    # فحص النطاق مع nmap
    nmap -sn $NETWORK_BASE.0/24 --max-rate=30 -T3 > scan_results.txt 2>&1
    
    echo ""
    echo "="*65
    echo "📋 نتائج الفحص:"
    echo "="*65
    
    # عرض النتائج
    if [ -f scan_results.txt ]; then
        echo "📱 الأجهزة المكتشفة:"
        echo ""
        
        # البحث عن النتائج الإيجابية
        grep -E "Nmap scan report|Host is up" scan_results.txt | while read line; do
            echo "   ✅ $line"
        done
        
        # عدد الأجهزة
        DEVICE_COUNT=$(grep -c "Nmap scan report" scan_results.txt)
        echo ""
        echo "📊 إجمالي الأجهزة المكتشفة: $DEVICE_COUNT"
        
    else
        echo "❌ لم يتم العثور على ملف النتائج"
    fi
    
else
    echo "❌ لم يتم العثور على عنوان IP"
    echo "💡 تأكد من اتصال WiFi"
fi

echo "="*65
echo "💾 تم حفظ التفاصيل في: scan_results.txt"
echo "="*65

echo ""
echo "📝 الملاحظات:"
echo "• عنوان IP الذي ظهر أعلاه هو لجهازك الرئيسي"
echo "• الأجهزة الأخرى ستظهر بعنوان IP مختلف"
echo "• احفظ هذه العناوين لاستخدامها في ملف التكوين"
echo "="*65