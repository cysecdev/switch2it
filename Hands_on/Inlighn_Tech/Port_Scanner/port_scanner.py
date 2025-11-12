import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

def get_banner_from_socket(sock, try_http=False):
    try:
        sock.settimeout(1.5)
        if try_http:
            try:
                sock.sendall(b"GET / HTTP/1.0\r\nHost: \r\n\r\n")
            except Exception:
                pass
        data = sock.recv(2048)
        return data.decode(errors="ignore").strip()
    except Exception:
        return ""

def scan_tcp(ip, port, try_http=False):
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        res = s.connect_ex((ip, port))
        if res == 0:
            try:
                service = socket.getservbyport(port, "tcp")
            except OSError:
                service = "Unknown"
            banner = get_banner_from_socket(s, try_http=try_http)
            return (port, "tcp", service, banner, "Open")
        else:
            return (port, "tcp", "", "", "Closed")
    except Exception as e:
        return (port, "tcp", "", f"ERR:{e}", "Error")
    finally:
        if s:
            s.close()

def scan_udp(ip, port):
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1.5)
        try:
            s.sendto(b"\x00", (ip, port))
        except Exception:
            pass
        try:
            data, _ = s.recvfrom(2048)
            banner = data.decode(errors="ignore").strip()
            return (port, "udp", "Unknown", banner, "Open")
        except socket.timeout:
            return (port, "udp", "Unknown", "", "Open|Filtered")
        except Exception as e:
            return (port, "udp", "Unknown", f"ERR:{e}", "Error")
    finally:
        if s:
            s.close()

def infer_os(open_entries):
    ports = {p for p, _, _, _ in open_entries}
    banners = " ".join((b or "").lower() for _, _, _, b in open_entries)
    if any(p in ports for p in (135, 139, 445, 3389)):
        return "Windows (heuristic)"
    if any(p in ports for p in (22, 80, 443, 8080)) or any(k in banners for k in ("openssh", "apache", "nginx")):
        return "Linux/Unix (heuristic)"
    if 161 in ports:
        return "Network Device / IoT (heuristic)"
    return "Unknown"

def print_open_table(results):
    """Print table with only open ports (TCP/UDP)."""
    open_rows = [r for r in results if r[4] in ("Open", "Open|Filtered")]
    if not open_rows:
        print(f"\n{YELLOW}No open ports found in range.{RESET}")
        return

    print()
    print(f"{'Port':<8}{'Proto':<8}{'Service':<15}{'Status':<15}{'Banner/Notes'}")
    print("-" * 100)
    for port, proto, service, banner, status in sorted(open_rows, key=lambda x: (x[0], x[1])):
        status_col = status
        if status == "Open":
            status_col = f"{GREEN}{status}{RESET}"
        elif status == "Open|Filtered":
            status_col = f"{YELLOW}{status}{RESET}"
        elif status == "Error":
            status_col = f"{RED}{status}{RESET}"
        short_banner = banner.splitlines()[0][:80] if banner else ""
        print(f"{str(port):<8}{proto:<8}{service:<15}{status_col:<15}{short_banner}")
    print("-" * 100)

def main():
    print("=== Port Scanner ===")
    try:
        target = input("Enter target IP or hostname: ").strip()
        start_port = int(input("Enter start port (e.g. 1): ").strip())
        end_port = int(input("Enter end port (e.g. 1024): ").strip())

        udp_choice = input("Include UDP scan? (Y/N): ").strip().lower()
        do_udp = udp_choice.startswith("y")

        try:
            ip = socket.gethostbyname(target)
        except socket.gaierror:
            print("[!] Invalid hostname/IP")
            return

        print(f"\n[+] Scanning {target} ({ip}) ports {start_port} to {end_port}")
        start_time = datetime.now()

        total_ports = end_port - start_port + 1
        tcp_results = []
        udp_results = []

        with ThreadPoolExecutor(max_workers=100) as ex:
            futures = {ex.submit(scan_tcp, ip, port, True): port for port in range(start_port, end_port + 1)}
            for i, fut in enumerate(as_completed(futures), start=1):
                tcp_results.append(fut.result())
                sys.stdout.write(f"\rTCP progress: {i}/{total_ports} ports scanned")
                sys.stdout.flush()
        sys.stdout.write("\n")

        if do_udp:
            with ThreadPoolExecutor(max_workers=50) as ex:
                futures = {ex.submit(scan_udp, ip, port): port for port in range(start_port, end_port + 1)}
                for i, fut in enumerate(as_completed(futures), start=1):
                    udp_results.append(fut.result())
                    sys.stdout.write(f"\rUDP progress: {i}/{total_ports} ports probed")
                    sys.stdout.flush()
            sys.stdout.write("\n")

        combined = tcp_results + udp_results
        print_open_table(combined)

        open_tcp = [(p, proto, svc, b) for (p, proto, svc, b, st) in tcp_results if st == "Open"]
        os_guess = infer_os(open_tcp)

        total_open = sum(1 for (_, _, _, _, st) in combined if st == "Open")
        total_open_filtered = sum(1 for (_, _, _, _, st) in combined if st == "Open|Filtered")
        duration = datetime.now() - start_time

        print("\nSummary:")
        print(f"  Ports scanned: {total_ports}")
        if do_udp:
            print(f"  UDP probed: {total_ports}")
        print(f"  Open: {total_open}")
        print(f"  Open|Filtered: {total_open_filtered}")
        print(f"  OS guess: {CYAN}{os_guess}{RESET}")
        print(f"\n[+] Scan completed in: {duration}")

    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user.")
        sys.exit()
    except ValueError:
        print("[!] Invalid input. Ports must be integers.")
        sys.exit()
    except Exception as e:
        print(f"[!] An error occurred: {e}")

if __name__ == "__main__":
    main()
