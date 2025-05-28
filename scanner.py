import socket
import threading
import json
import csv
from tqdm import tqdm
from fpdf import FPDF

def scan_port(host, port, results):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))
            if result == 0:
                results.append(port)
    except Exception:
        pass

def save_results_json(results, filename="scan_results.json"):
    with open(filename, "w") as f:
        json.dump({"open_ports": results}, f, indent=4)

def save_results_csv(results, filename="scan_results.csv"):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Open Ports"])
        for port in results:
            writer.writerow([port])

def save_results_pdf(results, filename="scan_results.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Port Scan Results", ln=True, align="C")
    for port in results:
        pdf.cell(200, 10, txt=f"Open Port: {port}", ln=True)
    pdf.output(filename)

if __name__ == "__main__":
    host = socket.gethostbyname(input("Enter host to scan: "))
    start_port = int(input("Start port: "))
    end_port = int(input("End port: "))

    open_ports = []
    threads = []

    print(f"\nScanning {host} from port {start_port} to {end_port}...\n")
    for port in tqdm(range(start_port, end_port + 1)):
        thread = threading.Thread(target=scan_port, args=(host, port, open_ports))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    open_ports.sort()
    print(f"\nOpen ports: {open_ports}")

    save_results_json(open_ports)
    save_results_csv(open_ports)
    save_results_pdf(open_ports)