#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kivy Interface for Stealth Network Intelligence
Beautiful GUI for the mobile monitoring system
"""

import os
import sys
import threading
import time
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.popup import Popup
from kivy.metrics import dp

# Try to import the stealth module
try:
    from stealth_network_spy_fixed import StealthNetworkSpy
    STEALTH_AVAILABLE = True
except ImportError:
    STEALTH_AVAILABLE = False
    print("⚠️ Stealth module not found. Some features will be limited.")

class StealthNetworkGUI:
    def __init__(self):
        self.spy_system = None
        self.monitoring_active = False
        self.log_data = []
        self.device_count = 0
        self.activity_count = 0
        
    def start_stealth_monitoring(self):
        """Start stealth monitoring in background thread"""
        if not STEALTH_AVAILABLE:
            self.add_log("❌ Stealth module not available")
            return
            
        try:
            self.spy_system = StealthNetworkSpy()
            self.monitoring_active = True
            
            # Start monitoring in separate thread
            def monitor_loop():
                self.spy_system.start_mobile_monitoring()
            
            monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
            monitor_thread.start()
            
            self.add_log("✅ Stealth monitoring started successfully")
            self.add_log("📱 Monitoring mobile network activities...")
            
        except Exception as e:
            self.add_log(f"❌ Failed to start monitoring: {e}")
    
    def stop_stealth_monitoring(self):
        """Stop stealth monitoring"""
        if self.spy_system:
            self.spy_system.running = False
        self.monitoring_active = False
        self.add_log("🛑 Stealth monitoring stopped")
    
    def add_log(self, message):
        """Add log message to the interface"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.log_data.append(log_entry)
        
        # Update UI (this should be called from the main thread)
        if hasattr(self, 'update_log_display'):
            Clock.schedule_once(lambda dt: self.update_log_display(), 0)
    
    def simulate_intelligence(self):
        """Simulate intelligence gathering for demo purposes"""
        demo_activities = [
            "📱 WhatsApp detected - COMMUNICATION",
            "🌐 Facebook accessed - SOCIAL_MEDIA", 
            "📺 YouTube stream detected - STREAMING",
            "💬 Telegram activity - COMMUNICATION",
            "🎮 Mobile game detected - GAMING",
            "📊 192.168.1.5 connected - DEVICE_ACTIVITY",
            "🔍 DNS query: google.com",
            "📡 Network scan completed - 3 devices found"
        ]
        
        for activity in demo_activities:
            time.sleep(1)
            self.add_log(activity)
            self.device_count = min(self.device_count + 1, 6)
            self.activity_count += 1

class MainInterface(BoxLayout):
    def __init__(self, **kwargs):
        super(MainInterface, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(20)
        self.spacing = dp(15)
        
        self.gui = StealthNetworkGUI()
        
        # Set window size for mobile
        Window.size = (400, 700)
        
        self.create_interface()
    
    def create_interface(self):
        """Create the main interface"""
        
        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
        header.add_widget(Label(text='🕵️ Stealth Network Intelligence', 
                               font_size='18sp', 
                               size_hint_x=0.8))
        
        self.status_label = Label(text='🔴 Inactive', 
                                 font_size='14sp', 
                                 color=(1, 0.3, 0.3, 1),
                                 size_hint_x=0.2)
        header.add_widget(self.status_label)
        self.add_widget(header)
        
        # Control buttons
        button_layout = GridLayout(cols=2, size_hint_y=None, height=dp(100))
        
        self.start_button = Button(text='🚀 Start Monitoring', 
                                  font_size='14sp',
                                  background_color=(0.2, 0.8, 0.2, 1))
        self.start_button.bind(on_press=self.start_monitoring)
        button_layout.add_widget(self.start_button)
        
        self.stop_button = Button(text='🛑 Stop Monitoring', 
                                 font_size='14sp',
                                 background_color=(0.8, 0.2, 0.2, 1),
                                 disabled=True)
        self.stop_button.bind(on_press=self.stop_monitoring)
        button_layout.add_widget(self.stop_button)
        
        self.add_widget(button_layout)
        
        # Statistics
        stats_layout = GridLayout(cols=3, size_hint_y=None, height=dp(80))
        
        self.devices_label = Label(text='📱 Devices: 0', font_size='12sp')
        stats_layout.add_widget(self.devices_label)
        
        self.activities_label = Label(text='📊 Activities: 0', font_size='12sp')
        stats_layout.add_widget(self.activities_label)
        
        self.risk_label = Label(text='⚠️ Risk: Low', font_size='12sp', color=(0.2, 0.8, 0.2, 1))
        stats_layout.add_widget(self.risk_label)
        
        self.add_widget(stats_layout)
        
        # Tabbed interface
        tab_panel = TabbedPanel()
        
        # Main Monitoring Tab
        main_tab = BoxLayout(orientation='vertical', padding=dp(10))
        
        # Progress bar for monitoring status
        self.progress_bar = ProgressBar(max=100, value=0, size_hint_y=None, height=dp(20))
        main_tab.add_widget(self.progress_bar)
        
        # Log display
        self.log_scroll = ScrollView(size_hint_y=1)
        self.log_layout = BoxLayout(orientation='vertical', size_hint_y=None, padding=dp(10))
        self.log_layout.bind(minimum_height=self.log_layout.setter('height'))
        
        for i in range(10):  # Initial placeholder
            label = Label(text=f"📋 System ready for monitoring...", 
                         size_hint_y=None, height=dp(30))
            self.log_layout.add_widget(label)
        
        self.log_scroll.add_widget(self.log_layout)
        main_tab.add_widget(self.log_scroll)
        
        tab_panel.add_widget(main_tab)
        
        # Intelligence Report Tab
        report_tab = BoxLayout(orientation='vertical', padding=dp(10))
        
        self.report_text = TextInput(text='Intelligence reports will appear here...', 
                                    multiline=True, 
                                    readonly=True, 
                                    font_size='12sp')
        report_tab.add_widget(self.report_text)
        
        tab_panel.add_widget(report_tab)
        
        # Settings Tab
        settings_tab = BoxLayout(orientation='vertical', padding=dp(10))
        
        settings_text = """🔧 Settings & Configuration:

📊 Monitoring Intervals:
• Network Scan: 15 seconds
• Process Check: 10 seconds  
• Browser Analysis: 20 seconds
• System Analysis: 60 seconds

🎯 Detection Categories:
• Social Media (Facebook, Instagram, WhatsApp)
• Streaming Services (YouTube, Netflix, Spotify)
• Communication Apps (Telegram, Discord, Slack)
• Mobile Games (PUBG, Free Fire, Mobile Legends)

🔐 Security Features:
• Local data encryption
• SQLite database storage
• No external data transmission
• Privacy-focused design

⚠️ Limitations:
• Works on device only
• Cannot monitor other devices without root
• Limited by Android security policies
"""
        
        settings_label = Label(text=settings_text, 
                              font_size='11sp', 
                              text_size=(None, None),
                              halign='left',
                              valign='top',
                              size_hint_y=1)
        settings_tab.add_widget(settings_label)
        
        tab_panel.add_widget(settings_tab)
        self.add_widget(tab_panel)
        
        # Footer
        footer = Label(text='🔒 Privacy-First | 🕵️ Stealth Mode | 📱 Mobile Optimized', 
                      font_size='10sp',
                      size_hint_y=None, 
                      height=dp(30))
        self.add_widget(footer)
    
    def start_monitoring(self, instance):
        """Start monitoring with GUI feedback"""
        self.start_button.disabled = True
        self.stop_button.disabled = False
        self.status_label.text = '🟢 Active'
        self.status_label.color = (0.2, 0.8, 0.2, 1)
        
        # Start monitoring in background
        def start_background():
            self.gui.start_stealth_monitoring()
            
            # Update progress
            for i in range(101):
                if not self.monitoring_active:
                    break
                Clock.schedule_once(lambda dt: self.progress_bar.__setattr__('value', i), 0)
                time.sleep(0.1)
        
        thread = threading.Thread(target=start_background, daemon=True)
        thread.start()
    
    def stop_monitoring(self, instance):
        """Stop monitoring"""
        self.start_button.disabled = False
        self.stop_button.disabled = True
        self.status_label.text = '🔴 Inactive'
        self.status_label.color = (1, 0.3, 0.3, 1)
        
        self.gui.stop_stealth_monitoring()
        self.progress_bar.value = 0
    
    def update_log_display(self):
        """Update the log display with new entries"""
        self.log_layout.clear_widgets()
        
        # Show last 20 log entries
        recent_logs = self.gui.log_data[-20:]
        for log_entry in recent_logs:
            label = Label(text=log_entry, 
                         size_hint_y=None, 
                         height=dp(25),
                         font_size='10sp',
                         text_size=(Window.width - 40, None))
            self.log_layout.add_widget(label)
        
        # Update statistics
        self.devices_label.text = f"📱 Devices: {self.gui.device_count}"
        self.activities_label.text = f"📊 Activities: {self.gui.activity_count}"
        
        # Auto-scroll to bottom
        Clock.schedule_once(lambda dt: setattr(self.log_scroll, 'scroll_y', 0), 0)

class StealthIntelligenceApp(App):
    def build(self):
        self.title = "Stealth Network Intelligence"
        return MainInterface()
    
    def on_start(self):
        """Called when app starts"""
        # Add welcome message
        if hasattr(self.root, 'gui'):
            self.root.gui.add_log("🚀 Stealth Network Intelligence App Started")
            self.root.gui.add_log("📱 Ready for mobile network monitoring")
            self.root.gui.add_log("🔧 Click 'Start Monitoring' to begin")
    
    def on_pause(self):
        """Called when app is paused"""
        return True  # Keep the app running in background
    
    def on_resume(self):
        """Called when app resumes from pause"""
        pass

if __name__ == '__main__':
    StealthIntelligenceApp().run()