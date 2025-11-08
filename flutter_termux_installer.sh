#!/bin/bash
# flutter_termux_installer.sh - مثبت Flutter في Termux
# مُطور بواسطة MiniMax Agent

echo "🚀 مثبت Flutter في Termux"
echo "========================="
echo "تأكد من تشغيل هذا السكريبت في Termux فقط"
echo ""

# التحقق من وجود Termux
if ! command -v pkg &> /dev/null; then
    echo "❌ هذا السكريبت مصمم للعمل مع Termux فقط"
    echo "📱 يرجى تثبيت Termux من F-Droid أو Google Play"
    exit 1
fi

echo "✅ تم التحقق من Termux"

# تحديث النظام
echo "📦 تحديث النظام..."
pkg update -y && pkg upgrade -y

# تثبيت الأدوات الأساسية
echo "🛠️ تثبيت الأدوات المطلوبة..."
pkg install git wget unzip curl openjdk-17 android-tools -y

# إنشاء مجلد العمل
echo "📁 إنشاء مجلد العمل..."
WORK_DIR="$HOME/flutter_dev"
mkdir -p "$WORK_DIR" && cd "$WORK_DIR"

# تحديد إصدار Flutter
FLUTTER_VERSION="3.24.3"
FLUTTER_URL="https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_${FLUTTER_VERSION}-stable.tar.xz"

# التحقق من وجود Flutter
if [ -d "$WORK_DIR/flutter" ]; then
    echo "🔄 Flutter موجود مسبقاً. تحديث..."
    cd flutter && git pull
else
    # تحميل Flutter
    echo "📥 تحميل Flutter SDK v$FLUTTER_VERSION..."
    wget "$FLUTTER_URL" -O flutter.tar.xz
    
    # استخراج الملف
    echo "📂 استخراج الملفات..."
    tar xf flutter.tar.xz
    rm flutter.tar.xz
fi

# إعداد PATH
echo "⚙️ إعداد البيئة..."
FLUTTER_PATH="$WORK_DIR/flutter/bin"

# إضافة Flutter إلى PATH
if ! echo $PATH | grep -q "$FLUTTER_PATH"; then
    echo 'export PATH="$PATH:$FLUTTER_PATH"' >> ~/.bashrc
fi

# تحديث PATH للجلسة الحالية
export PATH="$PATH:$FLUTTER_PATH"

# التحقق من التثبيت
echo "🔍 التحقق من التثبيت..."
flutter --version

if [ $? -eq 0 ]; then
    echo "✅ تم تثبيت Flutter بنجاح!"
    
    # قبول تراخيص Android
    echo "📄 قبول تراخيص Android..."
    yes | flutter doctor --android-licenses || true
    
    # فحص الحالة
    echo "🔍 فحص حالة Flutter:"
    flutter doctor
    
    # إنشاء مشروع تجريبي
    echo "🎯 إنشاء مشروع تجريبي..."
    flutter create test_app
    cd test_app
    
    echo ""
    echo "🎉 تم الإعداد بنجاح!"
    echo ""
    echo "📋 الخطوات التالية:"
    echo "1. شغل: flutter doctor"
    echo "2. شغل: cd test_app && flutter run"
    echo "3. لتطوير الكود، استخدم Acode أو محرر نصوص"
    echo ""
    echo "📁 مجلد العمل: $WORK_DIR"
    echo "🌐 للحصول على المساعدة: flutter --help"
else
    echo "❌ فشل في تثبيت Flutter"
    echo "💡 جرب تشغيل السكريبت مرة أخرى"
    exit 1
fi

# إنشاء ملف مساعدة سريع
cat > ~/flutter_help.sh << 'EOF'
#!/bin/bash
echo "🚀 Flutter Help - Termux"
echo "======================="
echo ""
echo "أوامر Flutter الأساسية:"
echo "- إنشاء مشروع: flutter create my_app"
echo "- تشغيل المشروع: flutter run"
echo "- بناء APK: flutter build apk"
echo "- فحص الحالة: flutter doctor"
echo "- تنظيف المشروع: flutter clean"
echo "- تحديث المكتبات: flutter pub get"
echo ""
echo "مجلد العمل: $HOME/flutter_dev"
echo "للتحديث: source ~/.bashrc"
EOF

chmod +x ~/flutter_help.sh
echo "📜 تم إنشاء ملف المساعدة: ~/flutter_help.sh"