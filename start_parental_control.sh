#!/bin/bash
echo "بدء تشغيل نظام المراقبة الأبوية..."
cd "$(dirname "$0")"
python3 ParentalControlSystem.py
read -p "اضغط Enter للمتابعة..."
