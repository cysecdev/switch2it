from scapy.all import ARP, Ether, srp
import socket
import ipaddress
import csv
from datetime import datetime
from tabulate import tabulate

TIMEOUT = 3
DEFAULT_FILENAME = "avl-net.csv"

def build_arp(cidr):
    try:
        ipaddress.ip_network(cidr, strict=False)
        packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=cidr)
        return packet
    except Exception as e:
        print(f"[!] Invalid CIDR: {e}")
        return None

def resolve_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return "Unknown"

def scan_network(cidr):
    packet = build_arp(cidr)
    if packet is None:
        return []

    print(f"[+] Scanning hosts in network {cidr} (waiting for replies)...")
    answered = srp(packet, timeout=TIMEOUT, verbose=0)[0]

    results = []
    scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for sent, received in answered:
        ip = received.psrc
        mac = received.hwsrc
        hostname = resolve_hostname(ip)
        results.append({"IP": ip, "MAC": mac, "Hostname": hostname, "ScanTime": scan_time})
    return results

def print_table(rows):
    if not rows:
        print("[!] No devices found.")
        return
    headers = ["IP", "MAC", "Hostname", "ScanTime"]
    table = [[r["IP"], r["MAC"], r["Hostname"], r["ScanTime"]] for r in rows]
    print("\n[+] Scan Results:\n")
    print(tabulate(table, headers=headers, tablefmt="github"))

def save_csv_default(rows):
    fields = ["IP", "MAC", "Hostname", "ScanTime"]
    try:
        with open(DEFAULT_FILENAME, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        print(f"[+] Saved results to: {DEFAULT_FILENAME}")
    except Exception as e:
        print(f"[!] Could not save CSV: {e}")


def main():
    cidr = input("Enter CIDR (e.g., 192.168.1.0/24): ").strip()
    rows = scan_network(cidr)
    print_table(rows)

    if rows:
        choice = input("\nDo you want to save results as CSV? (y/n): ").strip().lower()
        if choice == "y":
            save_csv_default(rows)

if __name__ == "__main__":
    main()
