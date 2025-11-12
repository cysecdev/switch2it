# 🔎 Subdomain Scanner

A lightweight **Python-based subdomain scanner** that discovers live subdomains of a given target domain using `requests` and `threading`. This project demonstrates basic **reconnaissance** techniques used in penetration testing and SOC analysis.

---

## 📌 Objective
The purpose of this tool is to:
- Automate **subdomain enumeration**.
- Identify live subdomains responding under a target domain.
- Save discovered results into an output file for further analysis.

---

## 🧩 Script Working


- **Load candidates:** Reads `subdomains.txt` into a list of subdomain prefixes.
- **User input:** Prompts for the target domain (e.g., `example.com`).
- **Threaded scanning:** Creates a thread for each subdomain to check `https://{subdomain}.{domain}` concurrently.
- **Check subdomains:** Each thread:

  Sends a GET request with a short timeout.
  If status code < 400, writes the URL to `discovered_subdomains.txt`.
  Ignores exceptions (DNS errors, connection issues, SSL problems).

- **Thread-safe writes:** Uses a `lock` to prevent multiple threads writing to the file simultaneously.
- **Completion:** Main thread waits for all threads (`join`) and prints a message when done.

---

## ⚙️ Requirements
- Python 3.x
- Libraries:  
```bash
pip install requests
```

---

## 📂 Project Structure
```
subdomain_scanner.py      # Main script
subdomains.txt            # Input file with possible subdomains
discovered_subdomains.txt # Output file with discovered subdomains
README.md                 # Project README (this file)
docs/                     # PDF &images
```

---

## ▶️ Usage 

1. Clone or download the project folder.
2. Make sure `subdomains.txt` exists with entries like:
```
www
mail
dev
test
```
3. Run the script:
```bash
python subdomain_scanner.py
```
4. Enter the target domain when prompted:
```
Enter the target domain: example.com
```
5. The tool will start scanning and print discovered subdomains:
```
[+] Discovered subdomain: https://www.example.com
[+] Discovered subdomain: https://mail.example.com
```
6. All results are saved in:
```
discovered_subdomains.txt
```
---

## Tips
- The script currently tries only `https`. If a host serves only `http`, it won't be detected. Consider adding an `http` fallback for broader coverage.  
- Threading is simple and effective for small lists; for thousands of names, consider a worker pool or async approach to manage resources.  
- Keep `subdomains.txt` clean (no empty lines) to avoid wasted threads. 

---

## 🔐 Use Case
- **Penetration Testing** → Enumerating potential attack surfaces.  
- **SOC Teams** → Monitoring which subdomains are active and may be vulnerable.  
- **Learning** → Builds understanding of reconnaissance and automation in cybersecurity.


