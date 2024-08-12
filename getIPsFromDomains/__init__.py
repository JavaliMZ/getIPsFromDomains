#!/usr/bin/python3

import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import tqdm
from tabulate import tabulate
from termcolor import colored  # type: ignore

def get_ip_addresses(domain):
    try:
        info = socket.getaddrinfo(domain, None, family=socket.AF_UNSPEC, proto=socket.IPPROTO_TCP)
        ip_addresses = list(set(addr[-1][0] for addr in info))
        return domain, ip_addresses
    except socket.gaierror:
        return domain, []

def resolve_domains(domains, max_workers=5):
    ip_dict = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_domain = {}

        for domain in domains:
            future = executor.submit(get_ip_addresses, domain)
            future_to_domain[future] = domain
            
        for future in tqdm.tqdm(as_completed(future_to_domain), total=len(domains), desc="Resolving domains"):
            domain = future_to_domain[future]
            try:
                domain, ip_addresses = future.result()
                ip_dict[domain] = ip_addresses
            except Exception as e:
                ip_dict[domain] = []
                print(f"Error resolving {domain}: {e}")

    return ip_dict


def pretty_print(results):
    table_data = []
    for domain, ips in results.items():
        ip_list = colored(", ".join(ips), "magenta") if ips else colored("No IP found", "blue")
        table_data.append([colored(domain, "green"), ip_list])
    print(tabulate(table_data, tablefmt="presto"))

def get_domains_from_file():
    with open(sys.argv[1], "r") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    domains = get_domains_from_file()
    resolved_ips = resolve_domains(domains)
    pretty_print(resolved_ips)

if __name__ == '__main__':
    main()
