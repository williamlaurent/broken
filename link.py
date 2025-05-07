import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
import signal
from colorama import Fore, Style, init

# Inisialisasi colorama
init(autoreset=True)

# Handle CTRL+C biar elegan
def handle_interrupt(sig, frame):
    print(f"\n{Fore.YELLOW}[!] Dihentikan oleh user. Keluar...\n")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_interrupt)

def print_banner():
    print(Fore.CYAN + Style.BRIGHT + r"""
  ____  ____   ___  _  _______ ____  _  _______
 | __ )|  _ \ / _ \| |/ / ____|  _ \| |/ / ____|
 |  _ \| | | | | | | ' /|  _| | |_) | ' /|  _|
 | |_) | |_| | |_| | . \| |___|  _ <| . \| |___
 |____/|____/ \___/|_|\_\_____|_| \_\_|\_\_____|
         404 Link Scanner by willmet and indonesiancodeparty
""")

def normalize_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        return "http://" + url  # default ke http
    return url

def get_links(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(Fore.RED + f"[!] Gagal akses {url} - {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    links = set()

    for tag in soup.find_all('a', href=True):
        full_url = urljoin(url, tag['href'])
        if full_url.startswith(("http://", "https://")):
            links.add(full_url)

    return links

def check_404(url):
    try:
        res = requests.head(url, allow_redirects=True, timeout=10)
        return res.status_code == 404
    except:
        return False

def scan_site(site, output_file):
    print(Fore.BLUE + f"\n[+] Scan: {site}")
    links = get_links(site)
    for link in links:
        if check_404(link):
            print(Fore.RED + f"[404] {link}")
            output_file.write(f"{link}\n")
        else:
            print(Fore.GREEN + f"[OK ] {link}")

if __name__ == "__main__":
    print_banner()

    try:
        with open("list.txt", "r") as f:
            targets = [normalize_url(line.strip()) for line in f if line.strip()]
    except FileNotFoundError:
        print(Fore.RED + "[!] list.txt tidak ditemukan.")
        sys.exit(1)

    with open("result.txt", "w") as out:
        for target in targets:
            scan_site(target, out)

    print(Fore.CYAN + "\n[✓] Selesai. Hasil 404 disimpan di result.txt\n")
