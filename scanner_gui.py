import tkinter as tk
from tkinter import messagebox
import socket
import threading

def scan_ports():
    host = entry_host.get()
    try:
        ip = socket.gethostbyname(host)
    except:
        messagebox.showerror("Error", "Invalid Host")
        return

    try:
        start = int(entry_start.get())
        end = int(entry_end.get())
    except:
        messagebox.showerror("Error", "Invalid Port Range")
        return

    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, f"Scanning {host} ({ip}) from port {start} to {end}...\n")

    def scan(port):
        s = socket.socket()
        s.settimeout(1)
        if s.connect_ex((ip, port)) == 0:
            result_box.insert(tk.END, f"Port {port} is open\n")
        s.close()

    for port in range(start, end + 1):
        threading.Thread(target=scan, args=(port,)).start()

root = tk.Tk()
root.title("TCP Port Scanner")

tk.Label(root, text="Host:").pack()
entry_host = tk.Entry(root)
entry_host.pack()

tk.Label(root, text="Start Port:").pack()
entry_start = tk.Entry(root)
entry_start.pack()

tk.Label(root, text="End Port:").pack()
entry_end = tk.Entry(root)
entry_end.pack()

tk.Button(root, text="Scan", command=scan_ports).pack(pady=10)
result_box = tk.Text(root, height=15, width=50)
result_box.pack()

root.mainloop()