import socket
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from utils import resolve_target, grab_banner
from services import get_service

open_ports = []

def scan_port(target, port, timeout):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        result = sock.connect_ex((target, port))
        if result == 0:
            service = get_service(port)
            banner = grab_banner(sock)

            output = f"[OPEN] Port {port} | {service} | {banner}"
            print(output)

            open_ports.append(output)

        sock.close()
    except:
        pass

def parse_ports(port_range):
    try:
        start, end = map(int, port_range.split("-"))
        return range(start, end + 1)
    except:
        print("Invalid port range. Use format: start-end (e.g. 1-1000)")
        exit()

def main():
    parser = argparse.ArgumentParser(description="Modular Python Port Scanner")
    parser.add_argument("-t", "--target", required=True, help="Target IP or domain")
    parser.add_argument("-p", "--ports", default="1-1024", help="Port range")
    parser.add_argument("-th", "--threads", type=int, default=100)
    parser.add_argument("-to", "--timeout", type=float, default=0.5)
    parser.add_argument("-o", "--output", help="Output file")

    args = parser.parse_args()

    target_ip = resolve_target(args.target)
    if not target_ip:
        print("Invalid target")
        return

    ports = parse_ports(args.ports)

    print("=" * 60)
    print(f"Target: {args.target} ({target_ip})")
    print(f"Started: {datetime.now()}")
    print("=" * 60)

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        for port in ports:
            executor.submit(scan_port, target_ip, port, args.timeout)

    print("\nScan complete.")

    if args.output:
        with open(args.output, "w") as f:
            for line in open_ports:
                f.write(line + "\n")

        print(f"Results saved to {args.output}")

if __name__ == "__main__":
    main()