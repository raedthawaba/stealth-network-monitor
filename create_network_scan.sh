#!/bin/bash

# إنشاء سكريبت بسيطة لفحص الشبكة
echo "🔍 إنشاء سكريبت فحص الشبكة..."

cat > network_scan.sh << 'EOF'
#!/bin/bash

echo "🌐 ماسح الشبكة للعثور على الأطفال الحقيقيين"
echo "="*50

# الحصول على عنوان IP المحلي
LOCAL_IP=$(hostname -I | awk '{print $1}')
echo "📍 عنوان IP الخاص بك: $LOCAL_IP"

# تحديد نطاق الشبكة
NETWORK_BASE=$(echo $LOCAL_IP | cut -d'.' -f1-3)
echo "🔍 نطاق الشبكة: $NETWORK_BASE.0/24"

echo "⏳ فحص الأجهزة المتصلة... (قد يستغرق دقيقتين)"

# فحص النطاق
nmap -sn $NETWORK_BASE.0/24 --max-rate=50 -T4 > scan_results.txt

echo ""
echo "="*60
echo "📋 نتائج الفحص:"
echo "="*60

# عرض النتائج
if [ -f scan_results.txt ]; then
    grep -E "Nmap scan report|Host is up" scan_results.txt
else
    echo "❌ لم يتم العثور على ملف النتائج"
fi

echo "="*60
echo "💾 تم حفظ التفاصيل في: scan_results.txt"
echo "="*60
EOF

chmod +x network_scan.sh
echo "✅ تم إنشاء سكريپت الفحص"
echo "🚀 لتشغيل الفحص، اكتب: ./network_scan.sh"