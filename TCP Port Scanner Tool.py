import socket
import threading

# Get user input for target host
host = socket.gethostbyname(input("\n[+] Enter host to scan: "))

# Get port range from user
start = int(input("\n[+] Enter starting port: "))
end = int(input("[+] Enter ending port: "))

print(f"\nScanning {host} from port {start} to {end}...")

def scan(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((host, port))
        if result == 0:
            print(f"[OPEN] Port {port}")
        s.close()
    except Exception as e:
        print(f"Error scanning port {port}: {e}")

# Multi-threaded scanning
for i in range(start, end + 1):
    t = threading.Thread(target=scan, args=(i,))
    t.start()
