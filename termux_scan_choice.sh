#!/bin/bash

echo "🎯 اختيار طريقة الفحص في Termux"
echo "="*40
echo "اختر الطريقة التي تريد تجربتها:"
echo "1. السكريپت المحدث (Bash)"
echo "2. سكريپت Python"
echo "3. فحص يدوي سريع"
echo ""
echo "اكتب رقم اختيارك (1, 2, أو 3):"

read choice

case $choice in
    1)
        echo "🔄 تشغيل السكريپت المحدث..."
        # كتابة وتشغيل السكريپت المحدث
        cat > fixed_network_scan.sh << 'EOF'
#!/bin/bash

echo "🌐 ماسح الشبكة - إصدار محدث"
echo "="*50

# استخدام الطرق المختلفة للحصول على IP
LOCAL_IP=""

# طريقة 1: ip route
if command -v ip &> /dev/null; then
    LOCAL_IP=$(ip route get 1.1.1.1 2>/dev/null | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' | head -1)
fi

# طريقة 2: ifconfig
if [ -z "$LOCAL_IP" ] && command -v ifconfig &> /dev/null; then
    LOCAL_IP=$(ifconfig 2>/dev/null | grep 'inet ' | grep -v '127.0.0.1' | head -1 | awk '{print $2}' | sed 's/addr://')
fi

# طريقة 3: default
if [ -z "$LOCAL_IP" ]; then
    LOCAL_IP="192.168.1.100"
    echo "⚠️ استخدام عنوان افتراضي"
fi

echo "📍 عنوان IP: $LOCAL_IP"

# فحص الشبكة
NETWORK_BASE=$(echo $LOCAL_IP | cut -d'.' -f1-3)
echo "🔍 نطاق الشبكة: $NETWORK_BASE.0/24"

nmap -sn $NETWORK_BASE.0/24 --max-rate=25 -T3 > scan_results.txt 2>&1

echo ""
echo "📋 النتائج:"
grep -E "Nmap scan|Host is up" scan_results.txt
DEVICE_COUNT=$(grep -c "Nmap scan" scan_results.txt 2>/dev/null || echo "0")
echo "📊 إجمالي الأجهزة: $DEVICE_COUNT"
echo "💾 محفوظ في: scan_results.txt"
EOF
        chmod +x fixed_network_scan.sh
        ./fixed_network_scan.sh
        ;;
    2)
        echo "🔄 تشغيل سكريپت Python..."
        python3 -c "
import subprocess
import re

def get_ip():
    try:
        result = subprocess.run(['ip', 'route'], capture_output=True, text=True, timeout=5)
        match = re.search(r'(\d+\.\d+\.\d+\.\d+)', result.stdout)
        if match:
            return match.group(1)
    except:
        pass
    return '192.168.1.100'

def scan(ip):
    base = '.'.join(ip.split('.')[:3])
    result = subprocess.run(['nmap', '-sn', f'{base}.0/24', '--max-rate=20'], 
                          capture_output=True, text=True, timeout=60)
    return result.stdout

ip = get_ip()
print(f'📍 IP: {ip}')
print('🔍 فحص الشبكة...')
results = scan(ip)
print('📋 النتائج:')
for line in results.split('\n'):
    if 'Nmap scan' in line:
        print(f'✅ {line.strip()}')
count = results.count('Nmap scan')
print(f'📊 إجمالي الأجهزة: {count}')
"
        ;;
    3)
        echo "📝 فحص يدوي سريع:"
        echo "1. اكتب: ip route get 1.1.1.1"
        echo "2. ستجد عنوان IP الخاص بك"
        echo "3. استبدل آخر رقم بـ 0-255 لفحص الشبكة"
        echo "4. مثال: إذا كان IP: 192.168.1.45"
        echo "   اكتب: nmap -sn 192.168.1.0/24"
        ;;
    *)
        echo "❌ اختيار غير صحيح"
        ;;
esac