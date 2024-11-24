#!/usr/bin/env python3

from argparse import ArgumentParser
from ipaddress import IPv4Network, collapse_addresses, ip_network
from sys import stdin, stdout, stderr
from typing import TextIO

ipv4 = []
ipv6 = []


def read_ips(f: TextIO):
    for l in f:
        ip = ip_network(l.strip())
        (ipv4 if isinstance(ip, IPv4Network) else ipv6).append(ip)


def write_ips(f: TextIO):
    for ips in [ipv4, ipv6]:
        for ip in collapse_addresses(ips):
            print(ip, file=f)


if __name__ == "__main__":
    # fmt: off
    parser = ArgumentParser(description="A simple script for minimizing ip blocklists")

    parser.add_argument("input", nargs="?", default="-",
        help="File with IP ranges in CIDR notation (default: stdin)")

    parser.add_argument("-o", "--output", default=None,
        help="File where the collapsed IP ranges should be written (default: stdout)")
    # fmt: on
    args = parser.parse_args()

    if args.input != "-":
        with open(args.input, encoding="utf-8") as f:
            read_ips(f)
    else:
        if stdin.isatty():
            print(
                "Reading IP ranges from stdin (CIDR notation, 1 per line).\nPress Ctrl + D to stop.",
                file=stderr,
            )
        read_ips(stdin)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            write_ips(f)
    else:
        write_ips(stdout)
