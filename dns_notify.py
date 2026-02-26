#!/usr/bin/env python3
"""Send a DNS NOTIFY message to a specified nameserver (RFC 1996)."""

import argparse
import socket
import sys

try:
    import dns.flags
    import dns.message
    import dns.opcode
    import dns.query
    import dns.rcode
    import dns.rdatatype
except ImportError:
    sys.exit("dnspython is required: pip install dnspython")


def resolve_host(server: str) -> str:
    """Resolve a hostname to an IP address, returning it unchanged if already an IP."""
    try:
        results = socket.getaddrinfo(server, None, proto=socket.IPPROTO_UDP)
        return results[0][4][0]
    except socket.gaierror as e:
        sys.exit(f"Error: cannot resolve '{server}': {e}")


def send_notify(zone: str, server: str, port: int, timeout: float, use_tcp: bool) -> None:
    ip = resolve_host(server)

    msg = dns.message.make_query(zone, dns.rdatatype.SOA)
    msg.set_opcode(dns.opcode.NOTIFY)
    msg.flags |= dns.flags.AA

    if use_tcp:
        response = dns.query.tcp(msg, ip, port=port, timeout=timeout)
    else:
        response = dns.query.udp(msg, ip, port=port, timeout=timeout)

    label = f"{server} ({ip})" if ip != server else server
    print(f"NOTIFY sent for zone '{zone}' to {label}:{port}")
    print(f"Response rcode: {dns.rcode.to_text(response.rcode())}")
    if response.answer:
        for rrset in response.answer:
            print(rrset)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Send a DNS NOTIFY message (RFC 1996) to a nameserver."
    )
    parser.add_argument("zone", help="Zone name to notify (e.g. example.com)")
    parser.add_argument("server", help="Target server hostname or IP address")
    parser.add_argument("-p", "--port", type=int, default=53, metavar="PORT",
                        help="DNS port (default: 53)")
    parser.add_argument("-t", "--timeout", type=float, default=5.0, metavar="SECS",
                        help="Query timeout in seconds (default: 5)")
    parser.add_argument("--tcp", action="store_true",
                        help="Use TCP instead of UDP")
    args = parser.parse_args()

    try:
        send_notify(args.zone, args.server, args.port, args.timeout, args.tcp)
    except dns.exception.Timeout:
        sys.exit(f"Error: timed out waiting for response from {args.server}:{args.port}")
    except OSError as e:
        sys.exit(f"Error: {e}")


if __name__ == "__main__":
    main()
