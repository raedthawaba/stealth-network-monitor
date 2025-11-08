# دليل مراقبة الراوتر للأطفال

## الشرط المسبق:
1. راوتر يدعم OpenWrt أو DD-WRT
2. أو راوتر بسجلات TCPdump
3. صلاحيات إدارية على الراوتر

## حل OpenWrt (الأفضل):

### 1. تثبيت OpenWrt:
- ابحث عن model راوترك على: https://openwrt.org/
- اتبع دليل التثبيت

### 2. تثبيت برامج المراقبة:
```bash
opkg update
opkg install tcpdump tcpdump-analyze
opkg install logread
opkg install kmod-ipt-conntrack-extra
```

### 3. إعداد سجلات المراقبة:
```bash
# إنشاء ملف السجلات
touch /tmp/netmonitor.log
chmod 666 /tmp/netmonitor.log

# بدء tcpdump للتسجيل
tcpdump -i br-lan -n -s 0 -w /tmp/netmonitor.pcap &

# عرض في الوقت الفعلي
tail -f /tmp/netmonitor.log
```

### 4. تحليل البيانات:
```bash
# تحليل ملفات PCAP
tcpdump -r /tmp/netmonitor.pcap -n | grep -E "(google|youtube|instagram|tiktok)"
```

## حل DD-WRT:
- تفعيل "System Log" في الإدارة
- تعيين "Log Level" إلى "Debug"
- حفظ السجلات للـ syslog

## تحليل البيانات المرصودة:
```sql
-- قاعدة بيانات تحليل السجلات
CREATE TABLE net_logs (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    source_ip TEXT,
    dest_ip TEXT,
    dest_port INTEGER,
    protocol TEXT,
    domain TEXT
);
```
