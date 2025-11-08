#!/bin/bash
# سكريبت تثبيت سريع لنظام الرقابة الأبوية على Termux
# Quick Setup Script for Parental Control System on Termux

echo "📱 تثبيت سريع لنظام الرقابة الأبوية على Termux"
echo "=================================================="

# التحقق من Termux
if [ ! -d "/data/data/com.termux/files" ]; then
    echo "❌ هذا السكريبت يجب أن يعمل على Termux فقط"
    echo "📲 قم بتحميل Termux من Google Play أو F-Droid"
    exit 1
fi

# تحديث النظام
echo "🔄 تحديث النظام..."
pkg update && pkg upgrade -y

# تثبيت Python
echo "🐍 تثبيت Python..."
pkg install python -y
pkg install python-dev -y
pkg install openssl -y

# التحقق من Python
python_version=$(python --version 2>&1)
echo "✅ Python مثبت: $python_version"

# تثبيت المكتبات
echo "📦 تثبيت المكتبات..."
pip install --upgrade pip
pip install requests flask simplejson 2>/dev/null || pip install --user requests flask simplejson

# إنشاء مجلد النظام
echo "📁 إنشاء مجلد النظام..."
cd ~ || exit 1
mkdir -p parental_control
cd parental_control

echo "📁 مجلد العمل: $(pwd)"

echo ""
echo "✅ تم التثبيت بنجاح!"
echo ""
echo "الخطوات التالية:"
echo "1. سيتم إنشاء ملف الإعدادات"
echo "2. سيتم إنشاء ملف النظام الرئيسي" 
echo "3. سيكون النظام جاهز للاستخدام"
echo ""
echo "🚀 لبدء الاستخدام: python3 mobile_parental_control.py"
echo ""
echo "اضغط Enter للمتابعة..."
read