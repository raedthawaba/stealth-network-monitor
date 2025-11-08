# دليل التطوير السريع - Flutter في Termux
# مُطور بواسطة MiniMax Agent

## 🚀 البدء السريع

### 1. تثبيت Flutter في Termux
```bash
# تحميل وتشغيل المثبت
chmod +x flutter_termux_installer.sh
./flutter_termux_installer.sh
```

### 2. إنشاء مشروع جديد
```bash
flutter create my_app
cd my_app
```

### 3. التطوير باستخدام Acode
1. انسخ مجلد المشروع إلى Acode
2. طور في Acode باستخدام Dart syntax highlighting
3. احفظ التغييرات
4. اختبر في Termux

---

## 📱 أوامر مفيدة للتطوير

### التطوير السريع:
```bash
# تشغيل مع hot reload
flutter run --debug --hot

# بناء APK سريع للاختبار
flutter build apk --debug

# تنظيف وإعادة تحميل
flutter clean && flutter pub get && flutter run
```

### إدارة المشروع:
```bash
# فحص حالة Flutter
flutter doctor

# فحص الأجهزة المتصلة
flutter devices

# تحديث المكتبات
flutter pub upgrade

# إضافة مكتبة جديدة
flutter pub add [package_name]
```

---

## 🎯 تطوير مع Acode

### إعداد Acode للمشروع:
1. **نسخ المشروع**:
   ```bash
   # في Termux
   cp -r my_app /sdcard/Download/flutter_projects/
   ```

2. **التطوير في Acode**:
   - افتح Acode
   - اذهب لمجلد `/sdcard/Download/flutter_projects/my_app`
   - طور الكود في `lib/main.dart`

3. **اختبار التغييرات**:
   ```bash
   # في Termux
   cd /sdcard/Download/flutter_projects/my_app
   flutter run
   ```

### نصائح Acode:
- فعّل Dart syntax highlighting
- استخدم theme داكن
- فعّل word wrap
- استخدم split view للملفات

---

## 🔧 حل المشاكل الشائعة

### مشكلة: "Android SDK not found"
```bash
export ANDROID_HOME=$PREFIX/share/android-sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin
```

### مشكلة: بطء Gradle
```bash
# زيادة ذاكرة Gradle
echo "org.gradle.jvmargs=-Xmx2048m" >> android/gradle.properties
```

### مشكلة: خطأ في البناء
```bash
# تنظيف شامل
flutter clean
flutter pub get
flutter doctor --android-licenses
```

---

## 📦 أمثلة سريعة

### إنشاء تطبيق جديد:
```bash
flutter create hello_world
cd hello_world
# طور في Acode
flutter run
```

### إضافة صفحة جديدة:
1. **في Acode**، أنشئ ملف `lib/pages/second_page.dart`
2. **أضف التنقل في main.dart**:
   ```dart
   Navigator.push(
     context,
     MaterialPageRoute(
       builder: (context) => SecondPage(),
     ),
   );
   ```

### إضافة مكتبة:
```bash
# في Termux
flutter pub add http
# في Acode، استخدم المكتبة
import 'package:http/http.dart' as http;
```

---

## 🎨 تخصيص التطبيق

### تغيير الألوان:
```dart
// في main.dart
theme: ThemeData(
  primarySwatch: Colors.purple, // غير اللون
  accentColor: Colors.amber,      // لون التمييز
),
```

### إضافة أيقونة مخصصة:
1. **أضف الأيقونة في pubspec.yaml**:
   ```yaml
   flutter:
     assets:
       - images/logo.png
   ```

2. **استخدمها في الكود**:
   ```dart
   Image.asset('images/logo.png', width: 100)
   ```

---

## 🚀 نشر التطبيق

### بناء APK للإصدار النهائي:
```bash
# بناء APK كامل
flutter build apk --release

# أو للأجهزة المتعددة
flutter build apk --split-per-abi
```

### التحقق من البناء:
```bash
# في مجلد android
./gradlew assembleRelease
```

---

## 📚 تعلم المزيد

### مصادر مفيدة:
- [Flutter Documentation](https://docs.flutter.dev/)
- [Dart Language Tour](https://dart.dev/guides/language/language-tour)
- [Flutter Widget Catalog](https://docs.flutter.dev/development/ui/widgets)
- [Pub.dev Packages](https://pub.dev/)

### قنوات يوتيوب مفيدة:
- Flutter Official
- Flutter Community
- CS Dojo (بالعربية)

---

## 🎉 الخلاصة

**تطوير Flutter في Termux + Acode = تجربة تطوير كاملة على الهاتف!**

### المميزات:
✅ **مجاني بالكامل**  
✅ **يعمل بدون حاسوب**  
✅ **تعلم مفاهيم Flutter**  
✅ **مشاريع عملية**  
✅ **نشر سريع**  

### ابدأ الآن مع المثال المرفق: `flutter_example/`

---

**🚀 طوّر أول تطبيق Flutter لك اليوم!**