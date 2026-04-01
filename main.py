import network
import socket
import time
from machine import Pin
from secrets import WIFI_SSID, WIFI_PASSWORD

# Motor setup
motor_in1 = Pin(14, Pin.OUT)
motor_in2 = Pin(15, Pin.OUT)

def motor_forward():
    motor_in1.value(1)
    motor_in2.value(0)

def motor_stop():
    motor_in1.value(0)
    motor_in2.value(0)

motor_stop() # Ensure motors are stopped at the start

# Connect pico to wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

print("Connecting to wifi")
while not wlan.isconnected() and wlan.status() >= 0:
    time.sleep(1)

# Grab the IP address assigned by your router
ip = wlan.ifconfig()[0]
print(f"Connected! Pico W IP Address: {ip}")

# Setup web server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
# This prevents "Address already in use" errors if you restart the script
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
s.bind(addr)
s.listen(1)
print('Listening for commands on', addr)

# Main loop
while True:
    try:
        cl, addr = s.accept()
        request = cl.recv(1024).decode('utf-8')
        
        # Parse the HTTP GET request
        if 'GET /?cmd=W' in request:
            motor_forward()
            print("Command received: W (Motor ON)")
        elif 'GET /?cmd=S' in request:
            motor_stop()
            print("Command received: S (Motor OFF)")

        # Send a HTTP response back so the client doesn't hang
        response = "HTTP/1.1 200 OK\r\nContent-type: text/plain\r\n\r\nCommand Executed"
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('Connection closed due to error.')