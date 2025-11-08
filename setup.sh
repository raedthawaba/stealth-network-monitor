#!/bin/bash
# setup.sh - سكريبت إعداد التطبيق في Termux
# مُطور بواسطة MiniMax Agent

echo "🚀 إعداد تطبيق التحكم عبر Termux"
echo "=================================="

# التحقق من وجود Termux
if ! command -v pkg &> /dev/null; then
    echo "❌ هذا السكريبت مصمم للعمل مع Termux فقط"
    echo "📱 يرجى تثبيت Termux من F-Droid أو Google Play"
    exit 1
fi

echo "✅ تم التحقق من Termux"

# تحديث النظام
echo "📦 تحديث الحزم..."
pkg update -y
pkg upgrade -y

# تثبيت Python إذا لم يكن مثبتاً
if ! command -v python &> /dev/null; then
    echo "🐍 تثبيت Python..."
    pkg install python -y
fi

# تثبيت pip إذا لم يكن مثبتاً
if ! command -v pip &> /dev/null; then
    echo "📋 تثبيت pip..."
    pkg install python-pip -y
fi

# تثبيت Flask
echo "🌐 تثبيت Flask..."
pip install flask

# تثبيت أدوات إضافية مفيدة
echo "🛠️ تثبيت أدوات إضافية..."
pkg install git curl wget nano vim -y

# إنشاء مجلد للتطبيق
echo "📁 إنشاء مجلد التطبيق..."
mkdir -p ~/termux_apps
cd ~/termux_apps

echo "✅ تم الإعداد بنجاح!"
echo ""
echo "📋 الخطوات التالية:"
echo "1. انسخ ملف termux_controlled_app.py إلى المجلد"
echo "2. شغل الأمر: python termux_controlled_app.py"
echo "3. افتح المتصفح واذهب إلى: http://localhost:5000"
echo ""
echo "🎉 استمتع بالتطبيق!"

# إنشاء ملف تشغيل سريع
cat > run_app.sh << 'EOF'
#!/bin/bash
echo "🚀 تشغيل تطبيق التحكم عبر Termux..."
echo "🌐 يمكنك الوصول للتطبيق على: http://localhost:5000"
echo "⏹️  اضغط Ctrl+C للإيقاف"
echo "=================================="
python termux_controlled_app.py
EOF

chmod +x run_app.sh
echo "📜 تم إنشاء ملف تشغيل سريع: run_app.sh"