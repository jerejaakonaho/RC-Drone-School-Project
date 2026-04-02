import socket
import time
import tkinter as tk
import threading

# UPDATE THIS to the IP address printed by your Pico in Thonny!
PICO_IP = '172.20.10.2' 
PORT = 80
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

is_w_pressed = False
running = True

def send_heartbeat():
    while running:
        try:
            if is_w_pressed:
                sock.sendto(b'W', (PICO_IP, PORT))
            else:
                sock.sendto(b'S', (PICO_IP, PORT))
        except OSError:
            # Handle error where IP is unreachable or on a different subnet
            pass
        time.sleep(0.05) # 20 Hz heartbeat

def on_press(event):
    global is_w_pressed
    if event.keysym.upper() == 'W':
        is_w_pressed = True

def on_release(event):
    global is_w_pressed
    if event.keysym.upper() == 'W':
        is_w_pressed = False

def on_closing():
    global running
    running = False
    try:
        sock.sendto(b'S', (PICO_IP, PORT))
    except Exception:
        pass
    root.destroy()

# A simple Tkinter GUI to capture key presses
root = tk.Tk()
root.title("Drone Controller")
root.geometry("350x150")

label = tk.Label(root, text=f"Connected to Pico ({PICO_IP})\n\nCLICK HERE TO FOCUS WINDOW\n\nHOLD 'W' to go forward.\nRELEASE to stop.", font=("Helvetica", 12))
label.pack(expand=True)

# Bind keys smoothly
root.bind('<KeyPress>', on_press)
root.bind('<KeyRelease>', on_release)
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start background network thread
t = threading.Thread(target=send_heartbeat, daemon=True)
t.start()

root.mainloop()