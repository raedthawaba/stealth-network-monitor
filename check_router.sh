#!/bin/bash
# فحص نوع الراوتر والميزات

echo "🔍 فحص الراوتر..."
echo "====================================="

# فحص الموديل
model=$(cat /sys/class/net/eth0/device 2>/dev/null | grep -o "vendor.*device.*" | head -1)
if [ -n "$model" ]; then
    echo "📱 موديل الراوتر: $model"
fi

# فحص IP الراوتر
router_ip=$(ip route | grep default | awk '{print $3}' | head -1)
echo "🖥️ IP الراوتر: $router_ip"

# فحص DNS
dns_ip=$(nslookup google.com | grep -A1 "Non-authoritative answer:" | tail -1 | awk '{print $3}')
if [ -n "$dns_ip" ]; then
    echo "🌐 DNS Server: $dns_ip"
fi

# اختبار اتصال بالراوتر
if ping -c 1 $router_ip > /dev/null 2>&1; then
    echo "✅ الراوتر متصل"
    
    # فحص Web Interface
    if curl -s http://$router_ip >/dev/null 2>&1; then
        echo "🌐 واجهة Web متاحة على: http://$router_ip"
    else
        echo "❌ واجهة Web غير متاحة"
    fi
    
else
    echo "❌ الراوتر غير متصل"
fi

echo "====================================="
echo "💡 للحصول على مراقبة حقيقية:"
echo "1. أدخل على واجهة الراوتر: http://$router_ip"
echo "2. ابحث عن 'Logs' أو 'System Log' أو 'OpenWrt'"
echo "3. إذا دعمت OpenWrt، يمكن تركيب برامج مراقبة"
