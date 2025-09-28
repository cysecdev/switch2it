# 🔎 Subdomain Scanner (Python)

A lightweight **Python-based subdomain scanner** that discovers live subdomains of a given target domain using `requests` and `threading`.  
This project demonstrates basic **reconnaissance** techniques used in penetration testing and SOC analysis.

---

## 📌 Objective
The purpose of this tool is to:
- Automate **subdomain enumeration**.
- Identify live subdomains responding under a target domain.
- Save discovered results into an output file for further analysis.

---

## 🧩 Script Explanation & How it Works

This section explains the main parts of `subdomain_scanner.py` and how the script executes step-by-step.

### Main components (brief)
- **`load_subdomains(filename)`**  
  Reads `subdomains.txt` and returns a list of candidate subdomain labels (one per line).  
- **`check_subdomain(subdomain, domain)`**  
  Builds an `https://{subdomain}.{domain}` URL and tries to request it using `requests`. If the response status code is less than 400, the URL is considered _alive_ and saved to the output file. Exceptions from `requests` are caught and ignored to keep the scanner running.  
- **Threading and `lock`**  
  The script creates a `threading.Thread` for each candidate and starts them concurrently. A `lock` ensures that only one thread writes to `discovered_subdomains.txt` at a time to prevent race conditions.  
- **`if __name__ == "__main__":`**  
  This guard runs `main()` when the script is executed directly (prevents automatic execution when imported).

### Execution flow (what happens when you run the script)
1. **Start** — You run `python subdomain_scanner.py`. The `main()` function starts.  
2. **Prepare output** — The script makes sure `discovered_subdomains.txt` exists (so appends won't fail).  
3. **Get target domain** — The script prompts: `Enter the target domain:` — you type `example.com`.  
4. **Load candidates** — It reads `subdomains.txt` to get possible prefixes like `www`, `mail`, `dev`.  
5. **Spawn threads** — For each candidate, a new thread runs `check_subdomain(sub, domain)`. Threads run in parallel to speed up the scan.  
6. **Check each subdomain** — Each thread:
   - Forms the URL `https://{candidate}.{domain}`.
   - Sends a GET request with a short timeout.
   - If the response returns and status code < 400, the script writes the URL to `discovered_subdomains.txt` (within a locked block).  
   - If the request fails (DNS error, connection refused, SSL issue, timeout, etc.), the exception is caught and ignored so scanning continues.  
7. **Finish** — The main thread waits for all worker threads to finish (`join()`), then prints a completion message and exits.

### Notes & small tips
- The script currently tries only `https`. If a host serves only `http`, it won't be detected. Consider adding an `http` fallback for broader coverage.  
- Threading is simple and effective for small lists; for thousands of names, consider a worker pool or async approach to manage resources.  
- Keep `subdomains.txt` clean (no empty lines) to avoid wasted threads.  
- You can add logging or record status codes and response times for richer output.

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
subdomains.txt            # Input file with possible subdomains (one per line)
discovered_subdomains.txt # Output file with discovered live subdomains
README.md                 # Project README (this file)
images/                   # Optional images (architecture, terminal, folder structure)
```

---

## 📊 Project Table

| **Section**        | **Contents** | **Explanation** |
|---------------------|--------------|-----------------|
| **Input**           | `subdomains.txt` | List of subdomains (e.g., `www`, `mail`, `dev`). |
| **User Input**      | Target domain | Example: `example.com`. |
| **Processing**      | Threaded HTTP(S) requests | Faster discovery using multiple threads. |
| **Output**          | `discovered_subdomains.txt` | List of discovered live subdomains. |
| **Tools/Libraries** | Python, `requests`, `threading` | Core technologies used. |
| **Error Handling**  | Skips unreachable hosts | Ensures smooth execution. |

---

## ▶️ Usage (Run Overview)

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

## 🔐 Use Case
- **Penetration Testing** → Enumerating potential attack surfaces.  
- **SOC Teams** → Monitoring which subdomains are active and may be vulnerable.  
- **Learning** → Builds understanding of reconnaissance and automation in cybersecurity.

---

