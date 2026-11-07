import argparse
import sys
from scanner import PortScanner
from exporter import export_results
from education import run_quiz


BANNER = r"""
======================================================================
  ____  ___   ____ _____   ____   ____  ___   ____  ____  _____ ____ 
 |  _ \/ _ \ / ___|_   _| / ___| / ___|/ _ \ / ___|/ ___|| ____|  _ \
 | |_) | | | | |    | |   \___ \| |   / /_\ | |  _| |  _ |  _| | |_) |
 |  __/| |_| | |___ | |    ___) | |___|  _  | |_| | |_| || |___|  _ < 
 |_|    \___/ \____||_|   |____/ \____|_| |_|\____|\____||_____|_| \_\
======================================================================
      Ethical Cybersecurity Port Scanner & Educational Tool
               [FOR AUTHORIZED PRACTICE & STUDY ONLY]
======================================================================
"""


def print_banner():
    print(BANNER)


def parse_args():
    parser = argparse.ArgumentParser(
        description="PortScannerPractice - Educational TCP Port Scanner & Security Quiz Tool",
        epilog="Use responsibly. Always obtain proper authorization before scanning any network."
    )
    
    parser.add_argument(
        "-t", "--target",
        type=str,
        help="Target IP address or domain name (e.g., 192.168.1.1 or scanme.nmap.org)"
    )
    parser.add_argument(
        "-p", "--ports",
        type=str,
        default="1-1024",
        help="Port range or single port (e.g., 80, 20-100, 1-1024). Default: 1-1024"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=2.0,
        help="Socket timeout in seconds per port. Default: 2.0"
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=10,
        help="Number of concurrent worker threads. Default: 10"
    )
    parser.add_argument(
        "-b", "--banner",
        action="store_true",
        help="Attempt service banner grabbing on open ports"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Output report file path (e.g., report.txt, scan.json, results.csv)"
    )
    parser.add_argument(
        "-f", "--format",
        type=str,
        choices=["txt", "json", "csv"],
        default="txt",
        help="Output report file format (txt, json, csv). Default: txt"
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Launch interactive console menu mode"
    )
    parser.add_argument(
        "-q", "--quiz",
        action="store_true",
        help="Run interactive cybersecurity port knowledge quiz"
    )

    return parser.parse_args()


def display_results(results):
    print("\n" + "=" * 70)
    print(f"{'PORT':<8}{'STATE':<8}{'SERVICE':<15}{'SECURITY IMPLICATION'}")
    print("=" * 70)

    if not results:
        print("[!] No open ports detected.")
        print("=" * 70 + "\n")
        return

    for item in results:
        port_str = f"{item['port']}/tcp"
        status = item.get('status', 'open').upper()
        service = item.get('service', 'unknown')
        implication = item.get('implication', 'N/A')
        banner = item.get('banner')

        print(f"{port_str:<8}{status:<8}{service:<15}{implication}")
        if banner:
            print(f"   └── Banner: {banner}")

    print("=" * 70)
    print(f"Total open ports found: {len(results)}\n")


def prompt_export(results):
    if not results:
        return

    try:
        print("[?] Would you like to export these results to a report file?")
        choice = input("    (y/N): ").strip().lower()

        if choice in ['y', 'yes']:
            filepath = input("[?] Enter report file name (default: scan_report.txt): ").strip()
            if not filepath:
                filepath = "scan_report.txt"

            fmt_choice = input("[?] Select format [txt/json/csv] (default: txt): ").strip().lower()
            if fmt_choice not in ['txt', 'json', 'csv']:
                fmt_choice = "txt"

            export_results(results, filepath, fmt_choice)
    except (EOFError, KeyboardInterrupt):
        print("\n[*] Export prompt skipped.")


def run_interactive_menu():
    print_banner()

    while True:
        print("\n=== Main Menu ===")
        print("1. Start TCP Port Scan")
        print("2. Take Port Security Quiz")
        print("3. Exit")

        try:
            choice = input("\nSelect an option (1-3): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[+] Exiting PortScannerPractice. Goodbye!")
            sys.exit(0)

        if choice == '1':
            _interactive_scan()
        elif choice == '2':
            run_quiz()
        elif choice == '3':
            print("\n[+] Exiting PortScannerPractice. Goodbye!")
            sys.exit(0)
        else:
            print("[!] Invalid option. Please enter 1, 2, or 3.")


def _interactive_scan():
    print("\n--- Configure TCP Port Scan ---")
    try:
        target = input("[?] Enter target IP address or hostname: ").strip()
        if not target:
            print("[!] Target cannot be empty.")
            return

        ports = input("[?] Enter port range or single port (default: 1-1024): ").strip()
        if not ports:
            ports = "1-1024"

        threads_input = input("[?] Enter thread count (default: 10): ").strip()
        threads = int(threads_input) if threads_input.isdigit() and int(threads_input) > 0 else 10

        timeout_input = input("[?] Enter timeout in seconds (default: 2.0): ").strip()
        try:
            timeout = float(timeout_input) if timeout_input else 2.0
        except ValueError:
            timeout = 2.0

        banner_choice = input("[?] Enable banner grabbing? (y/N): ").strip().lower()
        grab_banners = banner_choice in ['y', 'yes']
    except (EOFError, KeyboardInterrupt):
        print("\n[*] Scan configuration cancelled.")
        return

    print(f"\n[*] Starting scan on target: {target}")
    print(f"[*] Port specification: {ports} | Threads: {threads} | Timeout: {timeout}s | Banner Grabbing: {grab_banners}\n")

    scanner = PortScanner(
        target=target,
        ports=ports,
        timeout=timeout,
        threads=threads,
        grab_banners=grab_banners
    )

    results = scanner.run()
    display_results(results)
    prompt_export(results)
