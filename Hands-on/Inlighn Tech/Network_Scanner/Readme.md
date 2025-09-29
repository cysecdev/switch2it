# 🔎 Network Scanner

---

## OVERVIEW

A minimal, reliable local ARP-based network scanner written in Python.It sends a single ARP broadcast to a CIDR, collects replies, resolves hostnames, displays a neat table, and optionally saves results to csv file.

---

## OBJECTIVE

Build a small, easy-to-understand tool to discover active devices on a local network using ARP.
Goals:
* Teach ARP-based discovery and Scapy basics.
* Demonstrate reliable discovery using one broadcast packet.
* Show threading-free discovery (simpler and more reliable).
* Save results with a timestamp for reporting.
---

## SCRIPT FEATURES

* Sends one ARP broadcast for the entire CIDR (reliable device discovery).
* Parses replies to extract IP and MAC.
* Attempts reverse DNS lookup for each discovered IP (hostname or `Unknown`).
* Displays results in a readable table using `tabulate`.
* Optionally saves results (if you answer `y`) automatically as `avl-net.csv`.
* Adds ScanTime timestamp to each result row.

---

## ⚙️ Requirements

* Python 3.6+
* Python packages:`scapy `,`tabulate`

---

## 📂 Project Structure

```
Network_scanner/
├── network_scanner.py   # Main script
├── avl-net.csv          # scan result
├── Readme.md            # This file
└── docs/               # PDF & img files
```

---

## ▶️ Usage

Open terminal 
install python libraries :
```bash
pip install scapy tabulate

```
Run the main script :

```bash
python network_scanner.py
```
Follow prompts:

* **Enter CIDR** when prompted (e.g., `192.168.1.0/24`).
* Wait for script to collect **replies from hosts** and **results to get printed** in terminal.
* When asked: **Do you want to save results as CSV? (y/n):**
  Type `y` → results automatically saved to `avl-net.csv`
  Type `n` → no file

### Example output 


---

## 🔐 Use Case

* Quickly map devices on your home or lab LAN for inventory or lab setup.
* Capture a timestamped snapshot of active hosts before/after changes.
* Educational tool to learn ARP, Scapy, and basic network reconnaissance.


