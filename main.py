import sys
import signal
from cli import parse_args, print_banner, run_interactive_menu, display_results, prompt_export
from scanner import PortScanner
from exporter import export_results
from education import run_quiz


def signal_handler(sig, frame):
    print("\n\n[!] Operation cancelled by user. Exiting gracefully...")
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)

    args = parse_args()

    if getattr(args, 'interactive', False) or (not args.target and not args.quiz):
        run_interactive_menu()
        return

    if getattr(args, 'quiz', False):
        run_quiz()
        return

    if args.target:
        print_banner()
        print(f"[*] Target host: {args.target}")
        print(f"[*] Port range/list: {args.ports}")
        print(f"[*] Threads: {args.threads} | Timeout: {args.timeout}s | Banner Grabbing: {'Enabled' if args.banner else 'Disabled'}")
        print("[*] Starting scan...\n")

        scanner = PortScanner(
            target=args.target,
            ports=args.ports,
            timeout=args.timeout,
            threads=args.threads,
            grab_banners=args.banner
        )
        
        results = scanner.run()
        display_results(results)

        if getattr(args, 'output', None):
            export_results(results, args.output, getattr(args, 'format', 'txt'))
        else:
            prompt_export(results)


if __name__ == "__main__":
    main()
