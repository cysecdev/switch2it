import requests
import threading
import os

lock = threading.Lock()

OUTPUT_FILE = "discovered_subdomains.txt"

def load_subdomains(filename="subdomains.txt"):
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("subdomains.txt file not found!")
        return []
    
def check_subdomain(subdomain, domain):
    url = f"https://{subdomain}.{domain}"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code < 400:
            print(f"[+] Discovered subdomain: {url}")
            with lock:
                with open(OUTPUT_FILE, "a") as f:
                    f.write(url + "\n")
    except requests.RequestException as e:
        pass

def main():
    if not os.path.exists(OUTPUT_FILE):
        open(OUTPUT_FILE, "a").close()

    domain = input("Enter the target domain: ").strip()
    subdomains = load_subdomains()

    if not subdomains:
        print("No subdomains to scan.")
        return
    
    threads = []

    for sub in subdomains:
        t = threading.Thread(target=check_subdomain, args=(sub, domain))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()

    print(f"Scan complete. Discovered subdomains are saved in {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
