import network
import socket
import time
from machine import Pin

# Motor setup
motor_in1 = Pin(14, Pin.OUT)
motor_in2 = Pin(15, Pin.OUT)
led = Pin("LED", Pin.OUT) # Built-in LED on Pico W

def motor_forward():
    motor_in1.value(1)
    motor_in2.value(0)
    led.value(1)

def motor_stop():
    motor_in1.value(0)
    motor_in2.value(0)
    led.value(0)

motor_stop() # Ensure motors are stopped at the start

# Connect pico to wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

ssid = 'iPhone (Jere)'
password = '123456xx'
wlan.connect(ssid, password)

print(f"Connecting to {ssid}...")

# Wait until it actually connects or fails. 
# iPhone hotspots are slow to wake up and assign IP
max_wait = 20
while max_wait > 0:
    status = wlan.status()
    print(f"Status: {status}...")
    if status < 0 or status >= 3: # 3 = STAT_GOT_IP
        break
    max_wait -= 1
    time.sleep(1)

if wlan.status() != 3:
    print(f"\nConnection Failed (Status {wlan.status()}).")
    print("- Ensure 'Maximize Compatibility' is ON on your iPhone.")
    print("- Restart the Personal Hotspot screen on your iPhone.")
    raise SystemExit # Allow the script to exit so Thonny can take control

# Grab the IP address assigned by your router
ip = wlan.ifconfig()[0]
print(f"Connected! Pico W IP Address: {ip}")

# Setup UDP server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# This prevents "Address already in use" errors if you restart the script in Thonny 
try:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
except AttributeError:
    pass

# Bind to the address and port
s.bind(addr)
# Set a small timeout so recvfrom doesn't block forever
s.settimeout(0.1) 

print('Listening for UDP commands on', addr)

last_command_time = time.ticks_ms()
motor_active = False

# Main loop
while True:
    try:
        msg, client_addr = s.recvfrom(1024)
        request = msg.decode('utf-8').strip()
        
        if request == 'W':
            motor_forward()
            if not motor_active:
                print("Command received: W (Motor ON)")
            motor_active = True
            last_command_time = time.ticks_ms()
        elif request == 'S':
            if motor_active:
                motor_stop()
                print("Command received: S (Motor OFF)")
                motor_active = False
            last_command_time = time.ticks_ms()
            
    except OSError:
        # Timeout occurred, no data received in the 0.1s window
        pass
        
    # Failsafe check
    # time.ticks_diff safely handles the microsecond counter wrap-around
    if motor_active and time.ticks_diff(time.ticks_ms(), last_command_time) > 500:
        motor_stop()
        motor_active = False
        print("Failsafe: Connection lost or timeout, motor stopped")