#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تطبيق قابل للتحكم عبر Termux - مُطور بواسطة MiniMax Agent
يمكن التحكم به من خلال Termux وتطويره باستخدام Acode
"""

from flask import Flask, render_template_string, request, jsonify
import os
import json
import time
import subprocess
from datetime import datetime
import threading

app = Flask(__name__)

# متغيرات التطبيق
app_data = {
    'status': 'running',
    'last_command': '',
    'output': [],
    'system_info': {},
    'commands_executed': 0
}

# دالة للحصول على معلومات النظام
def get_system_info():
    """جلب معلومات النظام"""
    try:
        # معلومات البطارية
        battery_info = "غير متوفر"
        try:
            with open('/sys/class/power_supply/battery/capacity', 'r') as f:
                battery_level = f.read().strip()
                battery_info = f"{battery_level}%"
        except:
            pass

        # معلومات الذاكرة
        memory_info = "غير متوفر"
        try:
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read().splitlines()
                for line in meminfo:
                    if 'MemTotal' in line:
                        memory_info = line.split(':')[1].strip()
                        break
        except:
            pass

        app_data['system_info'] = {
            'battery': battery_info,
            'memory': memory_info,
            'storage': 'جاري الفحص...',
            'uptime': 'جاري الفحص...'
        }
    except Exception as e:
        app_data['system_info'] = {'error': str(e)}

# واجهة المستخدم الرئيسية
@app.route('/')
def dashboard():
    """لوحة التحكم الرئيسية"""
    get_system_info()
    
    template = '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>تطبيق التحكم عبر Termux</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
            }
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .status {
                display: inline-block;
                padding: 10px 20px;
                background: #4CAF50;
                border-radius: 20px;
                font-weight: bold;
            }
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .card {
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 20px;
                border: 1px solid rgba(255,255,255,0.2);
            }
            .card h3 {
                margin-bottom: 15px;
                color: #fff;
                font-size: 1.3em;
            }
            .system-info p {
                margin: 8px 0;
                padding: 8px;
                background: rgba(255,255,255,0.1);
                border-radius: 8px;
            }
            .command-form {
                display: flex;
                gap: 10px;
                margin-bottom: 15px;
            }
            .command-input {
                flex: 1;
                padding: 12px;
                border: none;
                border-radius: 8px;
                background: rgba(255,255,255,0.9);
                color: #333;
                font-size: 16px;
            }
            .btn {
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                background: #2196F3;
                color: white;
                cursor: pointer;
                font-weight: bold;
                transition: background 0.3s;
            }
            .btn:hover {
                background: #1976D2;
            }
            .output {
                background: #000;
                color: #00ff00;
                padding: 15px;
                border-radius: 8px;
                font-family: 'Courier New', monospace;
                max-height: 300px;
                overflow-y: auto;
                white-space: pre-wrap;
            }
            .stats {
                display: flex;
                justify-content: space-around;
                margin-top: 20px;
            }
            .stat {
                text-align: center;
            }
            .stat-number {
                font-size: 2em;
                font-weight: bold;
                color: #ffeb3b;
            }
            .refresh-btn {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: #ff9800;
                border: none;
                border-radius: 50%;
                width: 60px;
                height: 60px;
                color: white;
                font-size: 20px;
                cursor: pointer;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 تطبيق التحكم عبر Termux</h1>
                <div class="status">✅ {{ app_data.status.title() }}</div>
                <p>مُطور بواسطة MiniMax Agent | آخر تحديث: {{ app_data.system_info.get('last_update', 'غير متوفر') }}</p>
            </div>

            <div class="grid">
                <!-- معلومات النظام -->
                <div class="card">
                    <h3>📱 معلومات النظام</h3>
                    <div class="system-info">
                        <p><strong>🔋 البطارية:</strong> {{ app_data.system_info.get('battery', 'غير متوفر') }}</p>
                        <p><strong>💾 الذاكرة:</strong> {{ app_data.system_info.get('memory', 'غير متوفر') }}</p>
                        <p><strong>⚡ الحالة:</strong> {{ app_data.status.title() }}</p>
                        <p><strong>🕐 الوقت:</strong> {{ app_data.system_info.get('current_time', 'غير متوفر') }}</p>
                    </div>
                </div>

                <!-- لوحة التحكم -->
                <div class="card">
                    <h3>⚙️ لوحة التحكم</h3>
                    <form class="command-form" onsubmit="executeCommand(event)">
                        <input type="text" class="command-input" id="command" 
                               placeholder="أدخل الأمر (مثل: ls, ps, df)" required>
                        <button type="submit" class="btn">تنفيذ</button>
                    </form>
                    <div id="command-result"></div>
                </div>

                <!-- إخراج الأوامر -->
                <div class="card">
                    <h3>📋 آخر النتائج</h3>
                    <div class="output" id="output-display">
                        {{ app_data.output[-10:] | join('\n') if app_data.output else 'لا توجد نتائج بعد...' }}
                    </div>
                </div>
            </div>

            <div class="stats">
                <div class="stat">
                    <div class="stat-number">{{ app_data.commands_executed }}</div>
                    <div>الأوامر المُنفذة</div>
                </div>
                <div class="stat">
                    <div class="stat-number">{{ len(app_data.output) }}</div>
                    <div>سطر النتائج</div>
                </div>
                <div class="stat">
                    <div class="stat-number">{{ app_data.status.title() }}</div>
                    <div>حالة التطبيق</div>
                </div>
            </div>
        </div>

        <button class="refresh-btn" onclick="refreshPage()">🔄</button>

        <script>
            // تنفيذ الأوامر
            function executeCommand(event) {
                event.preventDefault();
                const command = document.getElementById('command').value;
                
                fetch('/execute', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({command: command})
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('command-result').innerHTML = 
                            '<div style="color: #4CAF50; margin-top: 10px;">✅ تم تنفيذ الأمر بنجاح</div>';
                        document.getElementById('output-display').textContent = data.output;
                        document.getElementById('command').value = '';
                    } else {
                        document.getElementById('command-result').innerHTML = 
                            '<div style="color: #f44336; margin-top: 10px;">❌ خطأ: ' + data.error + '</div>';
                    }
                })
                .catch(error => {
                    document.getElementById('command-result').innerHTML = 
                        '<div style="color: #f44336; margin-top: 10px;">❌ خطأ في الاتصال</div>';
                });
            }

            // تحديث الصفحة
            function refreshPage() {
                location.reload();
            }

            // تحديث تلقائي كل 5 ثواني
            setInterval(function() {
                fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    document.querySelector('.status').textContent = 
                        data.status === 'running' ? '✅ Running' : '⏸️ Stopped';
                });
            }, 5000);

            // إضافة تأثيرات
            document.addEventListener('DOMContentLoaded', function() {
                const cards = document.querySelectorAll('.card');
                cards.forEach((card, index) => {
                    setTimeout(() => {
                        card.style.opacity = '0';
                        card.style.transform = 'translateY(20px)';
                        card.style.transition = 'all 0.5s ease';
                        setTimeout(() => {
                            card.style.opacity = '1';
                            card.style.transform = 'translateY(0)';
                        }, 100);
                    }, index * 100);
                });
            });
        </script>
    </body>
    </html>
    '''
    
    app_data['system_info']['current_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    app_data['system_info']['last_update'] = datetime.now().strftime('%H:%M:%S')
    
    return render_template_string(template, app_data=app_data)

# تنفيذ الأوامر
@app.route('/execute', methods=['POST'])
def execute_command():
    """تنفيذ الأمر المرسل"""
    try:
        data = request.get_json()
        command = data.get('command', '').strip()
        
        if not command:
            return jsonify({'success': False, 'error': 'لم يتم تحديد أمر'})
        
        # تنفيذ الأمر
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            output = result.stdout if result.stdout else result.stderr
            if not output:
                output = "تم تنفيذ الأمر بنجاح (لا يوجد إخراج)"
                
        except subprocess.TimeoutExpired:
            output = "انتهت مهلة تنفيذ الأمر"
        except Exception as e:
            output = f"خطأ في تنفيذ الأمر: {str(e)}"
        
        # حفظ النتيجة
        app_data['last_command'] = command
        app_data['output'].append(f"[{datetime.now().strftime('%H:%M:%S')}] $ {command}")
        app_data['output'].append(output)
        app_data['output'].append("-" * 50)
        
        # الحفاظ على آخر 100 نتيجة فقط
        if len(app_data['output']) > 100:
            app_data['output'] = app_data['output'][-100:]
        
        app_data['commands_executed'] += 1
        
        return jsonify({
            'success': True, 
            'output': '\n'.join(app_data['output'][-20:]),
            'command': command
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# API للحصول على الحالة
@app.route('/api/status')
def api_status():
    """API للحصول على حالة التطبيق"""
    return jsonify({
        'status': app_data['status'],
        'commands_executed': app_data['commands_executed'],
        'output_lines': len(app_data['output']),
        'last_command': app_data['last_command']
    })

# API لإعادة التشغيل
@app.route('/api/restart')
def api_restart():
    """إعادة تشغيل التطبيق"""
    app_data['status'] = 'restarting'
    # إعادة تعيين البيانات
    app_data['output'] = ['تم إعادة تشغيل التطبيق في ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    app_data['status'] = 'running'
    return jsonify({'success': True, 'message': 'تم إعادة التشغيل بنجاح'})

# مسار اختبار بسيط
@app.route('/test')
def test():
    """اختبار بسيط للتطبيق"""
    return jsonify({
        'message': 'التطبيق يعمل بنجاح! 🚀',
        'timestamp': datetime.now().isoformat(),
        'developer': 'MiniMax Agent'
    })

if __name__ == '__main__':
    print("🚀 بدء تشغيل التطبيق...")
    print("📱 يمكنك التحكم في التطبيق عبر:")
    print("   - واجهة الويب: http://localhost:5000")
    print("   - Termux: python /path/to/termux_controlled_app.py")
    print("   - تطوير باستخدام Acode")
    print("=" * 50)
    
    # تشغيل التطبيق
    app.run(
        host='0.0.0.0',  # للسماح بالوصول من الشبكة المحلية
        port=5000,
        debug=False,  # وضع الإنتاج
        threaded=True
    )