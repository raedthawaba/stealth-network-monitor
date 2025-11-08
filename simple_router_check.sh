#!/bin/bash
# فحص بسيط للراوتر - يعمل في Termux

echo "🔍 فحص الراوتر والمعلومات..."
echo "================================"

# فحص IP الحالي
current_ip=$(hostname -I 2>/dev/null | awk '{print $1}')
echo "📱 IP جهازك: $current_ip"

# فحص الراوتر الافتراضي
router_ip=$(route -n 2>/dev/null | grep '0.0.0.0' | awk '{print $2}' | head -1)
if [ -z "$router_ip" ]; then
    router_ip="192.168.1.1"  # قيمة افتراضية شائعة
fi
echo "🖥️ IP الراوتر: $router_ip"

# فحص ما إذا كان الراوتر متصل
if ping -c 1 -W 1 $router_ip > /dev/null 2>&1; then
    echo "✅ الراوتر متصل: $router_ip"
    
    # محاولة فحص واجهة Web
    if curl -s -o /dev/null -w "%{http_code}" http://$router_ip | grep -q "200\|302\|301"; then
        echo "🌐 واجهة Web متاحة: http://$router_ip"
    fi
    
    # فحص معلومات الراوتر عبر Web
    echo "🔗 ادخل على هذه الروابط:"
    echo "   • http://$router_ip"
    echo "   • http://$router_ip/status"
    echo "   • http://$router_ip/admin"
    echo "   • http://$router_ip/setup"
else
    echo "❌ الراوتر غير متصل: $router_ip"
fi

echo "================================"
echo "💡 للمعلومات الكاملة:"
echo "1. ادخل على: http://$router_ip"
echo "2. ادخل على: http://$router_ip:8080"  # منفذ بديل
echo "3. ابحث عن: 'Logs', 'System Log', 'DHCP Clients'"
echo "4. أخبرني بنوع الراوتر!"