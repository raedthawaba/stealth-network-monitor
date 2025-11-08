#!/bin/bash
# flutter_helper.sh - أدوات مساعدة لتطوير Flutter في Termux
# مُطور بواسطة MiniMax Agent

FLUTTER_PROJECT_DIR="$HOME/flutter_projects"

# إنشاء مجلد المشاريع إذا لم يكن موجوداً
mkdir -p "$FLUTTER_PROJECT_DIR"

show_help() {
    echo "🚀 Flutter Helper - Termux"
    echo "=========================="
    echo ""
    echo "الأوامر المتاحة:"
    echo "1. new <project_name>    - إنشاء مشروع جديد"
    echo "2. run <project_name>    - تشغيل مشروع"
    echo "3. build <project_name>  - بناء APK"
    echo "4. clean <project_name>  - تنظيف مشروع"
    echo "5. doctor               - فحص حالة Flutter"
    echo "6. devices              - فحص الأجهزة المتصلة"
    echo "7. list                 - عرض جميع المشاريع"
    echo "8. help                 - عرض هذا المساعدة"
    echo ""
    echo "مثال: ./flutter_helper.sh new my_app"
}

create_project() {
    if [ -z "$1" ]; then
        echo "❌ يرجى تحديد اسم المشروع"
        echo "مثال: ./flutter_helper.sh new my_app"
        return 1
    fi
    
    PROJECT_NAME="$1"
    PROJECT_PATH="$FLUTTER_PROJECT_DIR/$PROJECT_NAME"
    
    echo "🎯 إنشاء مشروع جديد: $PROJECT_NAME"
    
    cd "$FLUTTER_PROJECT_DIR"
    flutter create "$PROJECT_NAME"
    
    if [ $? -eq 0 ]; then
        echo "✅ تم إنشاء المشروع بنجاح في: $PROJECT_PATH"
        echo "📁 انتقل للمشروع: cd $PROJECT_PATH"
        echo "🚀 لتشغيل المشروع: flutter run"
        
        # إنشاء ملف مساعدة للمشروع
        cat > "$PROJECT_PATH/flutter_help.txt" << EOF
Flutter Helper للمشروع: $PROJECT_NAME
========================================

الأوامر المفيدة:
- flutter run           : تشغيل المشروع
- flutter build apk     : بناء APK
- flutter clean         : تنظيف المشروع
- flutter pub get       : تحديث المكتبات
- flutter doctor        : فحص الحالة

للتطوير:
1. انسخ هذا المجلد إلى Acode
2. طور الكود في Acode
3. اختبر التغييرات في Termux

مجلد المشروع: $PROJECT_PATH
EOF
    else
        echo "❌ فشل في إنشاء المشروع"
        return 1
    fi
}

run_project() {
    if [ -z "$1" ]; then
        echo "❌ يرجى تحديد اسم المشروع"
        return 1
    fi
    
    PROJECT_PATH="$FLUTTER_PROJECT_DIR/$1"
    
    if [ ! -d "$PROJECT_PATH" ]; then
        echo "❌ المشروع غير موجود: $1"
        echo "💡 استخدم './flutter_helper.sh list' لعرض المشاريع المتاحة"
        return 1
    fi
    
    echo "🚀 تشغيل المشروع: $1"
    cd "$PROJECT_PATH"
    flutter run
}

build_project() {
    if [ -z "$1" ]; then
        echo "❌ يرجى تحديد اسم المشروع"
        return 1
    fi
    
    PROJECT_PATH="$FLUTTER_PROJECT_DIR/$1"
    
    if [ ! -d "$PROJECT_PATH" ]; then
        echo "❌ المشروع غير موجود: $1"
        return 1
    fi
    
    echo "🏗️ بناء APK للمشروع: $1"
    cd "$PROJECT_PATH"
    flutter build apk --debug
}

clean_project() {
    if [ -z "$1" ]; then
        echo "❌ يرجى تحديد اسم المشروع"
        return 1
    fi
    
    PROJECT_PATH="$FLUTTER_PROJECT_DIR/$1"
    
    if [ ! -d "$PROJECT_PATH" ]; then
        echo "❌ المشروع غير موجود: $1"
        return 1
    fi
    
    echo "🧹 تنظيف المشروع: $1"
    cd "$PROJECT_PATH"
    flutter clean && flutter pub get
    echo "✅ تم التنظيف بنجاح"
}

flutter_doctor() {
    echo "🔍 فحص حالة Flutter..."
    flutter doctor
}

list_devices() {
    echo "📱 فحص الأجهزة المتصلة..."
    flutter devices
}

list_projects() {
    echo "📂 المشاريع المتاحة:"
    echo "===================="
    
    if [ -d "$FLUTTER_PROJECT_DIR" ] && [ "$(ls -A "$FLUTTER_PROJECT_DIR")" ]; then
        for project in "$FLUTTER_PROJECT_DIR"/*; do
            if [ -d "$project" ]; then
                PROJECT_NAME=$(basename "$project")
                echo "📁 $PROJECT_NAME"
                echo "   المسار: $project"
                
                # فحص إذا كان مشروع Flutter صحيح
                if [ -f "$project/pubspec.yaml" ]; then
                    echo "   ✅ مشروع Flutter صحيح"
                else
                    echo "   ❌ ليس مشروع Flutter"
                fi
                echo ""
            fi
        done
    else
        echo "📭 لا توجد مشاريع بعد"
        echo "💡 أنشئ مشروع جديد باستخدام: ./flutter_helper.sh new <اسم_المشروع>"
    fi
}

setup_acode_info() {
    echo "📱 معلومات تطوير Flutter مع Acode"
    echo "=================================="
    echo ""
    echo "الخطوات:"
    echo "1. انسخ مشروعك إلى: /sdcard/Download/flutter_projects/"
    echo "2. افتح Acode واذهب للمجلد"
    echo "3. طور الكود في Acode"
    echo "4. اختبر في Termux باستخدام flutter run"
    echo ""
    echo "النصائح:"
    echo "- فعّل Dart syntax highlighting في Acode"
    echo "- استخدم theme داكن لراحة العين"
    echo "- احفظ التغييرات قبل الاختبار"
    echo "- استخدم split view للملفات المتعددة"
}

# معالجة الأوامر
case "$1" in
    "new")
        create_project "$2"
        ;;
    "run")
        run_project "$2"
        ;;
    "build")
        build_project "$2"
        ;;
    "clean")
        clean_project "$2"
        ;;
    "doctor")
        flutter_doctor
        ;;
    "devices")
        list_devices
        ;;
    "list")
        list_projects
        ;;
    "setup"|"acode")
        setup_acode_info
        ;;
    "help"|"")
        show_help
        ;;
    *)
        echo "❌ أمر غير معروف: $1"
        echo ""
        show_help
        exit 1
        ;;
esac