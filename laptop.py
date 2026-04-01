import urllib.request

# Config
# IP address printed by Pico W in Thonny
PICO_IP = '192.168.1.50' 

print(f"Attempting to send commands to http://{PICO_IP}")
print("W = Forward, S = Stop, Q = Quit")

while True:
    command = input("Enter command: ").strip().upper()
    
    if command == 'Q':
        print("Exiting...")
        # Optional: Send a stop command before exiting
        try:
            urllib.request.urlopen(f"http://{PICO_IP}/?cmd=S", timeout=2)
        except:
            pass
        break
        
    elif command in ['W', 'S']:
        url = f"http://{PICO_IP}/?cmd={command}"
        try:
            # Send the HTTP GET request
            response = urllib.request.urlopen(url, timeout=3)
            print(f"-> Sent '{command}' successfully.")
        except urllib.error.URLError as e:
            print(f"Network error. Is the Pico W turned on and connected to Wi-Fi?")
            print(f"Details: {e}")
        except Exception as e:
             print(f"An unexpected error occurred: {e}")
    else:
        print("Invalid command. Use W, S, or Q.")