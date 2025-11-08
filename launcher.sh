#!/bin/bash
# launcher.sh - مُشغل سريع للتطبيق
# مُطور بواسطة MiniMax Agent

echo "🚀 مُشغل تطبيق التحكم عبر Termux"
echo "================================"

# التحقق من وجود الملف
if [ ! -f "termux_controlled_app.py" ]; then
    echo "❌ لم يتم العثور على ملف termux_controlled_app.py"
    echo "📁 تأكد من وجود الملف في نفس المجلد"
    exit 1
fi

# التحقق من وجود Python
if ! command -v python &> /dev/null; then
    echo "❌ Python غير مثبت"
    echo "📦 قم بتشغيل: pkg install python"
    exit 1
fi

# التحقق من Flask
if ! python -c "import flask" &> /dev/null; then
    echo "❌ Flask غير مثبت"
    echo "📦 قم بتشغيل: pip install flask"
    exit 1
fi

echo "✅ تم التحقق من جميع المتطلبات"
echo "🌐 بدء تشغيل الخادم..."
echo "🔗 يمكن الوصول للتطبيق على: http://localhost:5000"
echo "⏹️  اضغط Ctrl+C للإيقاف"
echo "================================"

# تشغيل التطبيق
python termux_controlled_app.py