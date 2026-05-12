import subprocess
import psutil

def get_system_info():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    try:
        temp_data = subprocess.check_output("sensors", shell=True).decode()
        temp = next((line.split()[2] for line in temp_data.split('\n') if 'Core 0' in line), "N/A")
    except:
        temp = "N/A"
        
    return f"🌡 Temp: {temp}\n📊 CPU: {cpu}%\n🧠 RAM: {ram.percent}%\n💾 Disk: {disk.percent}%"

def get_logs(lines=20):
    try:
        return subprocess.check_output(['tail', '-n', str(lines), "/var/log/syslog"]).decode('utf-8')
    except:
        return "Не удалось прочитать системный лог."

def wake_pc():
    from config import NET_INT, MAC_ADDR
    try:
        subprocess.run(['sudo', 'etherwake', '-i', NET_INT, MAC_ADDR], check=True)
        return "⚡ Сигнал WoL отправлен!"
    except Exception as e:
        return f"❌ Ошибка WoL: {e}"

def reboot_server():
    subprocess.Popen(['sudo', 'reboot'])

def poweroff_server():
    subprocess.run(['sudo', 'poweroff', 'now'])
