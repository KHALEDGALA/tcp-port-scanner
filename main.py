
import socket
import errno
from concurrent.futures import ThreadPoolExecutor, as_completed

target = "127.0.0.1"

ports = [22, 80, 443, 3306, 5000, 8080]

MAX_WORKERS = 10
TIMEOUT = 1


def scan_port(target, port):
    try:
        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as sock:
            sock.settimeout(TIMEOUT)
            result = sock.connect_ex((target, port))

        if result == 0:
            status = "OPEN"
        elif result == errno.ECONNREFUSED:
            status = "CLOSED"
        else:
            status = f"FILTERED / ERROR ({result})"

        return port, status

    except socket.timeout:
        return port, "TIMEOUT"

    except OSError as error:
        return port, f"ERROR: {error}"


def main():
    print(f"\nTCP Port Scanner")
    print(f"Target: {target}")
    print(f"Ports to scan: {len(ports)}")
    print("-" * 40)

    results = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(scan_port, target, port)
            for port in ports
        ]

        for future in as_completed(futures):
            port, status = future.result()
            results.append((port, status))

    for port, status in sorted(results):
        print(f"Port {port:5} | {status}")

    print("-" * 40)
    print("Scan completed!")


if __name__ == "__main__":
    main()
