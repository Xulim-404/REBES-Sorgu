#!/usr/bin/env python3
import os
import sys
import socket
import json
import time
import sqlite3
import random
import subprocess
import re
import urllib.parse
from datetime import datetime

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        BLACK='';RED='';GREEN='';YELLOW='';BLUE='';MAGENTA='';CYAN='';WHITE='';RESET=''
    class Back:
        BLACK='';RED='';GREEN='';YELLOW='';BLUE='';MAGENTA='';CYAN='';WHITE='';RESET=''
    class Style:
        BRIGHT='';DIM='';NORMAL='';RESET_ALL=''

try:
    import requests
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

try:
    import dns.resolver
    DNS_OK = True
except ImportError:
    DNS_OK = False

try:
    import whois
    WHOIS_OK = True
except ImportError:
    WHOIS_OK = False

try:
    import phonenumbers
    from phonenumbers import carrier, geocoder, timezone
    PHONE_OK = True
except ImportError:
    PHONE_OK = False

C_RED = Fore.RED
C_GREEN = Fore.GREEN
C_YELLOW = Fore.YELLOW
C_BLUE = Fore.BLUE
C_MAGENTA = Fore.MAGENTA
C_CYAN = Fore.CYAN
C_WHITE = Fore.WHITE
C_RESET = Style.RESET_ALL
C_BRIGHT = Style.BRIGHT

DB_FILE = "xulim_story.db"

def logo():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"""{C_RED}{C_BRIGHT}
    ╔═══════════════════════════════════════════════════════════════════╗
    ║  {C_GREEN}██████╗ {C_RED}███████╗ {C_YELLOW}██████╗ {C_BLUE}███████╗ {C_MAGENTA}███████╗{C_RED}  ║
    ║  {C_GREEN}██╔══██╗{C_RED}██╔════╝{C_YELLOW}██╔══██╗{C_BLUE}██╔════╝ {C_MAGENTA}██╔════╝{C_RED}  ║
    ║  {C_GREEN}██████╔╝{C_RED}█████╗  {C_YELLOW}██████╔╝{C_BLUE}█████╗   {C_MAGENTA}███████╗{C_RED}  ║
    ║  {C_GREEN}██╔══██╗{C_RED}██╔══╝  {C_YELLOW}██╔══██╗{C_BLUE}██╔══╝   {C_MAGENTA}╚════██║{C_RED}  ║
    ║  {C_GREEN}██║  ██║{C_RED}███████╗{C_YELLOW}██████╔╝{C_BLUE}███████╗ {C_MAGENTA}███████║{C_RED}  ║
    ║  {C_GREEN}╚═╝  ╚═╝{C_RED}╚══════╝{C_YELLOW}╚═════╝ {C_BLUE}╚══════╝ {C_MAGENTA}╚══════╝{C_RED}  ║
    ║  {C_CYAN}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{C_RED}  ║
    ║  {C_CYAN}┃  {C_GREEN}XULİM OSINT ARACI v1.0{C_CYAN}                ┃{C_RED}  ║
    ║  {C_CYAN}┃  {C_YELLOW}Lider: Xulim{C_CYAN}                                        ┃{C_RED}  ║
    ║  {C_CYAN}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{C_RED}  ║
    ╚═══════════════════════════════════════════════════════════════════╝
{C_RESET}""")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS kisiler (
                    tc TEXT PRIMARY KEY,
                    ad TEXT,
                    soyad TEXT,
                    dogum_tarihi TEXT,
                    dogum_yeri TEXT,
                    meslek TEXT,
                    medeni_durum TEXT,
                    es_adi TEXT,
                    cocuk_sayisi INTEGER,
                    adres TEXT,
                    telefon TEXT,
                    email TEXT,
                    sosyal_medya TEXT,
                    egitim_durumu TEXT,
                    calistigi_kurum TEXT,
                    gelir_durumu TEXT,
                    sabika TEXT,
                    saglik_durumu TEXT,
                    hobiler TEXT,
                    dini_inanc TEXT,
                    siyasi_gorus TEXT,
                    boy_kilo TEXT,
                    kan_grubu TEXT,
                    aile_ozgecmisi TEXT,
                    onemli_olaylar TEXT,
                    son_guncelleme TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    c.execute("SELECT COUNT(*) FROM kisiler")
    if c.fetchone()[0] == 0:
        ornekler = [
            ("12345678901", "Ahmet", "Yılmaz", "1985-03-15", "İstanbul", "Mühendis", "Evli", "Ayşe", 2, "Kadıköy/İstanbul", "5551234567", "ahmet@mail.com", "@ahmet_yilmaz", "Üniversite", "Teknofest A.Ş.", "5000 TL", "Yok", "Sağlıklı", "Futbol, Kitap", "Müslüman", "Merkez", "175/75", "A Rh+", "Babası emekli öğretmen", "2018'de iş değiştirdi"),
            ("23456789012", "Ayşe", "Demir", "1990-07-22", "Ankara", "Öğretmen", "Bekar", "", 0, "Çankaya/Ankara", "5557654321", "ayse@mail.com", "@ayse_demir", "Yüksek Lisans", "MEB", "4500 TL", "Yok", "Astım", "Resim, Müzik", "Müslüman", "Sol", "165/60", "B Rh-", "Annesi ev hanımı, babası memur", "2020'de atandı"),
        ]
        c.executemany("INSERT INTO kisiler VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)", ornekler)
        conn.commit()
    conn.close()

def story_query(tc):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM kisiler WHERE tc = ?", (tc,))
    row = c.fetchone()
    conn.close()
    if row:
        return dict(zip([desc[0] for desc in c.description], row))
    return None

def sorgu1_ip():
    ip = input(f"{C_CYAN}IP adresi: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        if r.status_code == 200:
            d = r.json()
            if d['status'] == 'success':
                return f"""
{C_GREEN}[IP SORGUSU]{C_RESET}
{C_YELLOW}IP: {C_CYAN}{ip}
{C_YELLOW}Ülke: {C_CYAN}{d['country']} ({d['countryCode']})
{C_YELLOW}Bölge: {C_CYAN}{d['regionName']}
{C_YELLOW}Şehir: {C_CYAN}{d['city']}
{C_YELLOW}Zip: {C_CYAN}{d['zip']}
{C_YELLOW}Koordinat: {C_CYAN}{d['lat']}, {d['lon']}
{C_YELLOW}ISP: {C_CYAN}{d['isp']}
{C_YELLOW}Organizasyon: {C_CYAN}{d['org']}
{C_YELLOW}AS: {C_CYAN}{d['as']}
{C_YELLOW}Zaman: {C_CYAN}{d['timezone']}
"""
        return f"{C_RED}Hata {r.status_code}{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu2_dns_a():
    dom = input(f"{C_CYAN}Domain: {C_RESET}")
    if not DNS_OK: return "dnspython gerekli"
    try:
        ans = dns.resolver.resolve(dom, 'A')
        return f"{C_GREEN}[A KAYITLARI]{C_RESET}\n" + "\n".join([f"{C_YELLOW}{a}{C_RESET}" for a in ans])
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu3_dns_mx():
    dom = input(f"{C_CYAN}Domain: {C_RESET}")
    if not DNS_OK: return "dnspython gerekli"
    try:
        ans = dns.resolver.resolve(dom, 'MX')
        return f"{C_GREEN}[MX KAYITLARI]{C_RESET}\n" + "\n".join([f"{C_YELLOW}{a.exchange} (priority {a.preference}){C_RESET}" for a in ans])
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu4_dns_ns():
    dom = input(f"{C_CYAN}Domain: {C_RESET}")
    if not DNS_OK: return "dnspython gerekli"
    try:
        ans = dns.resolver.resolve(dom, 'NS')
        return f"{C_GREEN}[NS KAYITLARI]{C_RESET}\n" + "\n".join([f"{C_YELLOW}{a}{C_RESET}" for a in ans])
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu5_dns_txt():
    dom = input(f"{C_CYAN}Domain: {C_RESET}")
    if not DNS_OK: return "dnspython gerekli"
    try:
        ans = dns.resolver.resolve(dom, 'TXT')
        return f"{C_GREEN}[TXT KAYITLARI]{C_RESET}\n" + "\n".join([f"{C_YELLOW}{a.strings}{C_RESET}" for a in ans])
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu6_dns_cname():
    dom = input(f"{C_CYAN}Domain: {C_RESET}")
    if not DNS_OK: return "dnspython gerekli"
    try:
        ans = dns.resolver.resolve(dom, 'CNAME')
        return f"{C_GREEN}[CNAME KAYDI]{C_RESET}\n{C_YELLOW}{ans[0].target}{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu7_dns_ptr():
    ip = input(f"{C_CYAN}IP: {C_RESET}")
    if not DNS_OK: return "dnspython gerekli"
    try:
        ans = dns.resolver.resolve_address(ip)
        return f"{C_GREEN}[PTR KAYDI]{C_RESET}\n{C_YELLOW}{ans[0]}{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu8_whois_domain():
    dom = input(f"{C_CYAN}Domain: {C_RESET}")
    if not WHOIS_OK: return "whois kütüphanesi gerekli"
    try:
        w = whois.whois(dom)
        out = f"{C_GREEN}[WHOIS {dom}]{C_RESET}\n"
        for k,v in w.items():
            if v:
                if isinstance(v, list):
                    v = ', '.join(str(x) for x in v if x)
                if v:
                    out += f"{C_YELLOW}{k}: {C_CYAN}{v}{C_RESET}\n"
        return out
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu9_whois_ip():
    ip = input(f"{C_CYAN}IP: {C_RESET}")
    try:
        import ipwhois
        obj = ipwhois.IPWhois(ip)
        res = obj.lookup_rdap()
        return f"{C_GREEN}[WHOIS IP {ip}]{C_RESET}\n{C_YELLOW}ASN: {C_CYAN}{res['asn']}\n{C_YELLOW}ASN Ülke: {C_CYAN}{res['asn_country_code']}\n{C_YELLOW}ASN Açıklama: {C_CYAN}{res['asn_description']}\n{C_YELLOW}ISP: {C_CYAN}{res['network']['name']}\n{C_YELLOW}Ülke: {C_CYAN}{res['network']['country']}\n{C_YELLOW}CIDR: {C_CYAN}{res['network']['cidr']}"
    except ImportError:
        return f"{C_RED}ipwhois kütüphanesi gerekli. pip install ipwhois{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu10_alt_domain():
    dom = input(f"{C_CYAN}Domain: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"https://crt.sh/?q=%.{dom}&output=json", timeout=10)
        if r.status_code == 200:
            data = r.json()
            subs = set()
            for e in data:
                name = e['name_value']
                if '\n' in name:
                    for n in name.split('\n'):
                        subs.add(n.strip().lower())
                else:
                    subs.add(name.strip().lower())
            return f"{C_GREEN}[ALT DOMAINLER ({len(subs)})]{C_RESET}\n" + "\n".join([f"{C_YELLOW}{s}{C_RESET}" for s in sorted(subs)[:50]])
        return f"{C_RED}crtsh hatası {r.status_code}{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu11_reverse_ip():
    ip = input(f"{C_CYAN}IP: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"http://viewdns.info/reverseip/?host={ip}&t=1", headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
        if r.status_code == 200:
            html = r.text
            domains = re.findall(r'<td>([a-zA-Z0-9.-]+)</td><td>[0-9]+</td>', html)
            return f"{C_GREEN}[REVERSE IP (viewdns)]{C_RESET}\n" + "\n".join([f"{C_YELLOW}{d}{C_RESET}" for d in domains[:20]])
        return f"{C_RED}viewdns hatası {r.status_code}{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu12_port_tara():
    ip = input(f"{C_CYAN}IP: {C_RESET}")
    portlar = [21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080,8443]
    acik = []
    for p in portlar:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        if s.connect_ex((ip, p)) == 0:
            acik.append(p)
        s.close()
    return f"{C_GREEN}[AÇIK PORTLAR]{C_RESET}\n" + (", ".join(map(str, acik)) if acik else "Hiçbiri")

def sorgu13_ssl():
    dom = input(f"{C_CYAN}Domain: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"https://api.ssllabs.com/api/v3/analyze?host={dom}", timeout=15)
        if r.status_code == 200:
            d = r.json()
            if d['status'] == 'READY' or d['status'] == 'ERROR':
                out = f"{C_GREEN}[SSL LABS {dom}]{C_RESET}\n"
                for ep in d['endpoints']:
                    out += f"{C_YELLOW}Sunucu: {ep['ipAddress']} - Not: {ep.get('grade','?')}\n{C_CYAN}{ep.get('details','')}{C_RESET}\n"
                return out
            return f"{C_YELLOW}Analiz devam ediyor, tekrar dene.{C_RESET}"
        return f"{C_RED}SSL Labs hatası {r.status_code}{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu14_http_header():
    url = input(f"{C_CYAN}URL (http://...): {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(url, timeout=5, allow_redirects=False)
        out = f"{C_GREEN}[HTTP HEADER {url}]{C_RESET}\n"
        for k,v in r.headers.items():
            out += f"{C_YELLOW}{k}: {C_CYAN}{v}{C_RESET}\n"
        return out
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu15_banner():
    ip = input(f"{C_CYAN}IP: {C_RESET}")
    port = input(f"{C_CYAN}Port: {C_RESET}")
    try:
        s = socket.socket()
        s.settimeout(3)
        s.connect((ip, int(port)))
        s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = s.recv(1024).decode(errors='ignore')
        s.close()
        return f"{C_GREEN}[BANNER {ip}:{port}]{C_RESET}\n{C_CYAN}{banner}{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu16_github_user():
    user = input(f"{C_CYAN}GitHub kullanıcı adı: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"https://api.github.com/users/{user}")
        if r.status_code == 200:
            d = r.json()
            return f"""
{C_GREEN}[GITHUB {user}]{C_RESET}
{C_YELLOW}İsim: {C_CYAN}{d.get('name','?')}
{C_YELLOW}Bio: {C_CYAN}{d.get('bio','?')}
{C_YELLOW}Şirket: {C_CYAN}{d.get('company','?')}
{C_YELLOW}Konum: {C_CYAN}{d.get('location','?')}
{C_YELLOW}E-posta: {C_CYAN}{d.get('email','?')}
{C_YELLOW}Repolar: {C_CYAN}{d.get('public_repos')}
{C_YELLOW}Takipçi: {C_CYAN}{d.get('followers')}
{C_YELLOW}Blog: {C_CYAN}{d.get('blog','?')}
"""
        return f"{C_RED}Kullanıcı bulunamadı{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu17_github_repo():
    repo = input(f"{C_CYAN}Repo (kullanıcı/Repo): {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"https://api.github.com/repos/{repo}")
        if r.status_code == 200:
            d = r.json()
            return f"""
{C_GREEN}[GITHUB REPO {repo}]{C_RESET}
{C_YELLOW}Ad: {C_CYAN}{d.get('name')}
{C_YELLOW}Açıklama: {C_CYAN}{d.get('description','?')}
{C_YELLOW}Yıldız: {C_CYAN}{d.get('stargazers_count')}
{C_YELLOW}Fork: {C_CYAN}{d.get('forks_count')}
{C_YELLOW}Dil: {C_CYAN}{d.get('language','?')}
{C_YELLOW}Lisans: {C_CYAN}{d.get('license',{}).get('name','?')}
{C_YELLOW}Oluşturulma: {C_CYAN}{d.get('created_at')}
"""
        return f"{C_RED}Repo bulunamadı{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu18_twitter():
    user = input(f"{C_CYAN}Twitter kullanıcı adı: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"https://nitter.net/{user}", headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
        if r.status_code == 200:
            html = r.text
            isim = re.search(r'<a class="profile-card-fullname" href="[^"]*">([^<]+)</a>', html)
            bio = re.search(r'<div class="profile-bio">([^<]+)</div>', html)
            takip = re.search(r'<span class="profile-stat-num">([0-9,]+)</span>', html)
            return f"""
{C_GREEN}[TWITTER {user} (Nitter)]{C_RESET}
{C_YELLOW}İsim: {C_CYAN}{isim.group(1) if isim else '?'}
{C_YELLOW}Bio: {C_CYAN}{bio.group(1) if bio else '?'}
{C_YELLOW}Takipçi: {C_CYAN}{takip.group(1) if takip else '?'}
"""
        return f"{C_RED}Profil bulunamadı{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu19_instagram():
    user = input(f"{C_CYAN}Instagram kullanıcı adı: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"https://www.instagram.com/{user}/", headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
        if r.status_code == 200:
            html = r.text
            isim = re.search(r'<meta property="og:title" content="(.*?)"', html)
            desc = re.search(r'<meta property="og:description" content="(.*?)"', html)
            img = re.search(r'<meta property="og:image" content="(.*?)"', html)
            return f"""
{C_GREEN}[INSTAGRAM {user}]{C_RESET}
{C_YELLOW}İsim: {C_CYAN}{isim.group(1) if isim else '?'}
{C_YELLOW}Açıklama: {C_CYAN}{desc.group(1) if desc else '?'}
{C_YELLOW}Profil resmi: {C_CYAN}{img.group(1) if img else '?'}
"""
        return f"{C_RED}Profil bulunamadı{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu20_tiktok():
    user = input(f"{C_CYAN}TikTok kullanıcı adı: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"https://www.tiktok.com/@{user}", headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
        if r.status_code == 200:
            html = r.text
            isim = re.search(r'<meta property="og:title" content="(.*?)"', html)
            desc = re.search(r'<meta property="og:description" content="(.*?)"', html)
            img = re.search(r'<meta property="og:image" content="(.*?)"', html)
            return f"""
{C_GREEN}[TIKTOK @{user}]{C_RESET}
{C_YELLOW}İsim: {C_CYAN}{isim.group(1) if isim else '?'}
{C_YELLOW}Açıklama: {C_CYAN}{desc.group(1) if desc else '?'}
{C_YELLOW}Profil resmi: {C_CYAN}{img.group(1) if img else '?'}
"""
        return f"{C_RED}Profil bulunamadı{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu21_snapchat():
    user = input(f"{C_CYAN}Snapchat kullanıcı adı: {C_RESET}")
    return f"{C_YELLOW}Snapchat web profili yok, varsayalım ki {user} aktif.{C_RESET}"

def sorgu22_reddit():
    user = input(f"{C_CYAN}Reddit kullanıcı adı: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"https://www.reddit.com/user/{user}/about.json", headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
        if r.status_code == 200:
            d = r.json()['data']
            return f"""
{C_GREEN}[REDDIT u/{user}]{C_RESET}
{C_YELLOW}İsim: {C_CYAN}{d.get('subreddit',{}).get('title','?')}
{C_YELLOW}Karma: {C_CYAN}{d.get('total_karma')}
{C_YELLOW}Oluşturulma: {C_CYAN}{time.ctime(d.get('created_utc'))}
"""
        return f"{C_RED}Kullanıcı bulunamadı{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu23_youtube():
    kanal = input(f"{C_CYAN}YouTube kanal adı: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"https://www.youtube.com/@{kanal}", headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
        if r.status_code == 200:
            html = r.text
            isim = re.search(r'<meta property="og:title" content="(.*?)"', html)
            aciklama = re.search(r'<meta property="og:description" content="(.*?)"', html)
            return f"""
{C_GREEN}[YOUTUBE @{kanal}]{C_RESET}
{C_YELLOW}Kanal: {C_CYAN}{isim.group(1) if isim else '?'}
{C_YELLOW}Açıklama: {C_CYAN}{aciklama.group(1) if aciklama else '?'}
"""
        return f"{C_RED}Kanal bulunamadı{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu24_steam():
    steamid = input(f"{C_CYAN}Steam ID veya custom URL: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"https://steamcommunity.com/id/{steamid}?xml=1", timeout=10)
        if r.status_code == 200:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(r.text)
            def g(tag):
                e = root.find(tag)
                return e.text if e is not None else '?'
            return f"""
{C_GREEN}[STEAM {steamid}]{C_RESET}
{C_YELLOW}SteamID: {C_CYAN}{g('steamID')}
{C_YELLOW}Online: {C_CYAN}{g('onlineState')}
{C_YELLOW}Son görülme: {C_CYAN}{g('lastlogoff')}
{C_YELLOW}Ülke: {C_CYAN}{g('location')}
"""
        return f"{C_RED}Profil bulunamadı{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu25_twitch():
    user = input(f"{C_CYAN}Twitch kanal adı: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"https://www.twitch.tv/{user}", headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
        if r.status_code == 200:
            html = r.text
            isim = re.search(r'<meta property="og:title" content="(.*?)"', html)
            desc = re.search(r'<meta property="og:description" content="(.*?)"', html)
            return f"""
{C_GREEN}[TWITCH {user}]{C_RESET}
{C_YELLOW}Kanal: {C_CYAN}{isim.group(1) if isim else '?'}
{C_YELLOW}Açıklama: {C_CYAN}{desc.group(1) if desc else '?'}
"""
        return f"{C_RED}Kanal bulunamadı{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu26_discord():
    uid = input(f"{C_CYAN}Discord kullanıcı ID: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"https://discord.com/api/v9/users/{uid}", timeout=10)
        if r.status_code == 200:
            d = r.json()
            return f"""
{C_GREEN}[DISCORD {uid}]{C_RESET}
{C_YELLOW}Kullanıcı adı: {C_CYAN}{d.get('username')}#{d.get('discriminator')}
{C_YELLOW}Bot mu: {C_CYAN}{d.get('bot', False)}
"""
        return f"{C_RED}Kullanıcı bulunamadı{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu27_spotify():
    user = input(f"{C_CYAN}Spotify kullanıcı adı: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"https://open.spotify.com/user/{user}", headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
        if r.status_code == 200:
            html = r.text
            isim = re.search(r'<meta property="og:title" content="(.*?)"', html)
            desc = re.search(r'<meta property="og:description" content="(.*?)"', html)
            return f"""
{C_GREEN}[SPOTIFY {user}]{C_RESET}
{C_YELLOW}Profil: {C_CYAN}{isim.group(1) if isim else '?'}
{C_YELLOW}Açıklama: {C_CYAN}{desc.group(1) if desc else '?'}
"""
        return f"{C_RED}Kullanıcı bulunamadı{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu28_soundcloud():
    user = input(f"{C_CYAN}SoundCloud kullanıcı adı: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"https://soundcloud.com/{user}", headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
        if r.status_code == 200:
            html = r.text
            isim = re.search(r'<meta property="og:title" content="(.*?)"', html)
            desc = re.search(r'<meta property="og:description" content="(.*?)"', html)
            return f"""
{C_GREEN}[SOUNDCLOUD {user}]{C_RESET}
{C_YELLOW}Profil: {C_CYAN}{isim.group(1) if isim else '?'}
{C_YELLOW}Açıklama: {C_CYAN}{desc.group(1) if desc else '?'}
"""
        return f"{C_RED}Kullanıcı bulunamadı{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu29_medium():
    user = input(f"{C_CYAN}Medium kullanıcı adı: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"https://medium.com/@{user}", headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
        if r.status_code == 200:
            html = r.text
            isim = re.search(r'<meta property="og:title" content="(.*?)"', html)
            desc = re.search(r'<meta property="og:description" content="(.*?)"', html)
            return f"""
{C_GREEN}[MEDIUM @{user}]{C_RESET}
{C_YELLOW}Profil: {C_CYAN}{isim.group(1) if isim else '?'}
{C_YELLOW}Açıklama: {C_CYAN}{desc.group(1) if desc else '?'}
"""
        return f"{C_RED}Kullanıcı bulunamadı{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu30_devto():
    user = input(f"{C_CYAN}dev.to kullanıcı adı: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"https://dev.to/api/users/by_username?url={user}")
        if r.status_code == 200:
            d = r.json()
            return f"""
{C_GREEN}[DEV.TO {user}]{C_RESET}
{C_YELLOW}İsim: {C_CYAN}{d.get('name')}
{C_YELLOW}Bio: {C_CYAN}{d.get('summary')}
{C_YELLOW}Konum: {C_CYAN}{d.get('location')}
{C_YELLOW}Takipçi: {C_CYAN}{d.get('followers_count')}
"""
        return f"{C_RED}Kullanıcı bulunamadı{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu31_hackernews():
    user = input(f"{C_CYAN}HackerNews kullanıcı adı: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"https://hacker-news.firebaseio.com/v0/user/{user}.json")
        if r.status_code == 200:
            d = r.json()
            return f"""
{C_GREEN}[HACKERNEWS {user}]{C_RESET}
{C_YELLOW}Karma: {C_CYAN}{d.get('karma')}
{C_YELLOW}Oluşturulma: {C_CYAN}{time.ctime(d.get('created'))}
"""
        return f"{C_RED}Kullanıcı bulunamadı{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu32_producthunt():
    user = input(f"{C_CYAN}ProductHunt kullanıcı adı: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"https://www.producthunt.com/@{user}", headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
        if r.status_code == 200:
            html = r.text
            isim = re.search(r'<meta property="og:title" content="(.*?)"', html)
            desc = re.search(r'<meta property="og:description" content="(.*?)"', html)
            return f"""
{C_GREEN}[PRODUCTHUNT @{user}]{C_RESET}
{C_YELLOW}Profil: {C_CYAN}{isim.group(1) if isim else '?'}
{C_YELLOW}Açıklama: {C_CYAN}{desc.group(1) if desc else '?'}
"""
        return f"{C_RED}Kullanıcı bulunamadı{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu33_angellist():
    user = input(f"{C_CYAN}AngelList kullanıcı adı: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"https://angel.co/u/{user}", headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
        if r.status_code == 200:
            html = r.text
            isim = re.search(r'<meta property="og:title" content="(.*?)"', html)
            desc = re.search(r'<meta property="og:description" content="(.*?)"', html)
            return f"""
{C_GREEN}[ANGELCO {user}]{C_RESET}
{C_YELLOW}Profil: {C_CYAN}{isim.group(1) if isim else '?'}
{C_YELLOW}Açıklama: {C_CYAN}{desc.group(1) if desc else '?'}
"""
        return f"{C_RED}Kullanıcı bulunamadı{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu34_google_site():
    site = input(f"{C_CYAN}Site (ornek.com): {C_RESET}")
    terim = input(f"{C_CYAN}Aranacak kelime (boş geç): {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    q = f"site:{site}"
    if terim:
        q += f" {terim}"
    try:
        r = requests.get("https://www.google.com/search", params={'q':q}, headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
        if r.status_code == 200:
            sonuc_sayisi = re.search(r'Yaklaşık ([0-9,.]+) sonuç bulundu', r.text)
            return f"{C_GREEN}[GOOGLE SİTE:{site}]{C_RESET}\n{C_YELLOW}Sonuç: {C_CYAN}{sonuc_sayisi.group(1) if sonuc_sayisi else 'bilinmiyor'}{C_RESET}"
        return f"{C_RED}Google engelledi{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu35_bing():
    site = input(f"{C_CYAN}Site (ornek.com): {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get("https://www.bing.com/search", params={'q':f'site:{site}'}, headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
        if r.status_code == 200:
            sayi = re.search(r'([0-9,]+) sonuç', r.text)
            return f"{C_GREEN}[BING SİTE:{site}]{C_RESET}\n{C_YELLOW}Sonuç: {C_CYAN}{sayi.group(1) if sayi else 'bilinmiyor'}{C_RESET}"
        return f"{C_RED}Bing engelledi{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu36_yandex():
    site = input(f"{C_CYAN}Site (ornek.com): {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get("https://yandex.com/search/", params={'text':f'site:{site}'}, headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
        if r.status_code == 200:
            sayi = re.search(r'([0-9]+) sonuç', r.text)
            return f"{C_GREEN}[YANDEX SİTE:{site}]{C_RESET}\n{C_YELLOW}Sonuç: {C_CYAN}{sayi.group(1) if sayi else 'bilinmiyor'}{C_RESET}"
        return f"{C_RED}Yandex engelledi{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu37_baidu():
    site = input(f"{C_CYAN}Site (ornek.com): {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get("https://www.baidu.com/s", params={'wd':f'site:{site}'}, headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
        if r.status_code == 200:
            sayi = re.search(r'百度为您找到相关结果约([0-9,]+)个', r.text)
            return f"{C_GREEN}[BAIDU SİTE:{site}]{C_RESET}\n{C_YELLOW}Sonuç: {C_CYAN}{sayi.group(1) if sayi else 'bilinmiyor'}{C_RESET}"
        return f"{C_RED}Baidu engelledi{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu38_phone_detail():
    num = input(f"{C_CYAN}Telefon (90...): {C_RESET}")
    if not PHONE_OK: return "phonenumbers gerekli"
    try:
        n = phonenumbers.parse(num, "TR")
        tip = "Mobil" if phonenumbers.number_type(n) == phonenumbers.PhoneNumberType.MOBILE else "Sabit"
        gecerli = phonenumbers.is_valid_number(n)
        operator = carrier.name_for_number(n, "tr")
        bolge = geocoder.description_for_number(n, "tr")
        tz = timezone.time_zones_for_number(n)
        return f"""
{C_GREEN}[TELEFON DETAY]{C_RESET}
{C_YELLOW}Numara: {C_CYAN}{num}
{C_YELLOW}Geçerli: {C_CYAN}{gecerli}
{C_YELLOW}Tip: {C_CYAN}{tip}
{C_YELLOW}Operatör: {C_CYAN}{operator or '?'}
{C_YELLOW}Bölge: {C_CYAN}{bolge or '?'}
{C_YELLOW}Zaman dilimi: {C_CYAN}{', '.join(tz)}
"""
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu39_phone_operator():
    num = input(f"{C_CYAN}Telefon: {C_RESET}")
    if not PHONE_OK: return "phonenumbers gerekli"
    try:
        n = phonenumbers.parse(num, "TR")
        op = carrier.name_for_number(n, "tr")
        return f"{C_GREEN}[OPERATÖR]{C_RESET} {C_CYAN}{op or 'Bilinmiyor'}{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu40_phone_location():
    num = input(f"{C_CYAN}Telefon: {C_RESET}")
    if not PHONE_OK: return "phonenumbers gerekli"
    try:
        n = phonenumbers.parse(num, "TR")
        bolge = geocoder.description_for_number(n, "tr")
        return f"{C_GREEN}[KONUM]{C_RESET} {C_CYAN}{bolge or 'Bilinmiyor'}{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu41_phone_timezone():
    num = input(f"{C_CYAN}Telefon: {C_RESET}")
    if not PHONE_OK: return "phonenumbers gerekli"
    try:
        n = phonenumbers.parse(num, "TR")
        tz = timezone.time_zones_for_number(n)
        return f"{C_GREEN}[ZAMAN DİLİMİ]{C_RESET} {C_CYAN}{', '.join(tz)}{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu42_phone_type():
    num = input(f"{C_CYAN}Telefon: {C_RESET}")
    if not PHONE_OK: return "phonenumbers gerekli"
    try:
        n = phonenumbers.parse(num, "TR")
        tip = "Mobil" if phonenumbers.number_type(n) == phonenumbers.PhoneNumberType.MOBILE else "Sabit"
        return f"{C_GREEN}[HAT TİPİ]{C_RESET} {C_CYAN}{tip}{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu43_country_code():
    kod = input(f"{C_CYAN}Ülke kodu (+...): {C_RESET}")
    ulkeler = {
        "+90": "Türkiye", "+1": "ABD/Kanada", "+44": "İngiltere", "+49": "Almanya",
        "+33": "Fransa", "+39": "İtalya", "+34": "İspanya", "+7": "Rusya",
        "+86": "Çin", "+81": "Japonya", "+82": "Güney Kore", "+91": "Hindistan",
        "+55": "Brezilya", "+52": "Meksika", "+61": "Avustralya", "+31": "Hollanda",
        "+32": "Belçika", "+41": "İsviçre", "+46": "İsveç", "+47": "Norveç",
        "+45": "Danimarka", "+358": "Finlandiya", "+48": "Polonya", "+420": "Çekya",
        "+36": "Macaristan", "+40": "Romanya", "+359": "Bulgaristan", "+30": "Yunanistan",
        "+27": "Güney Afrika", "+20": "Mısır", "+966": "Suudi Arabistan", "+971": "BAE",
        "+98": "İran", "+964": "Irak", "+963": "Suriye", "+972": "İsrail",
        "+992": "Tacikistan", "+993": "Türkmenistan", "+994": "Azerbaycan", "+995": "Gürcistan",
        "+374": "Ermenistan", "+373": "Moldova", "+380": "Ukrayna", "+375": "Belarus",
    }
    return f"{C_GREEN}[ÜLKE]{C_RESET} {C_CYAN}{ulkeler.get(kod, 'Bulunamadı')}{C_RESET}"

def sorgu44_email_validate():
    email = input(f"{C_CYAN}E-posta: {C_RESET}")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return f"{C_RED}Geçersiz format{C_RESET}"
    return f"{C_GREEN}[E-POSTA FORMATI]{C_RESET} {C_CYAN}Geçerli{C_RESET}"

def sorgu45_email_mx():
    dom = input(f"{C_CYAN}Domain (ornek.com): {C_RESET}")
    if not DNS_OK: return "dnspython gerekli"
    try:
        ans = dns.resolver.resolve(dom, 'MX')
        return f"{C_GREEN}[MX KAYITLARI]{C_RESET}\n" + "\n".join([f"{C_YELLOW}{a.exchange}{C_RESET}" for a in ans])
    except Exception as e:
        return f"{C_RED}MX kaydı yok veya hata: {e}{C_RESET}"

def sorgu46_ip_geo_alt():
    ip = input(f"{C_CYAN}IP: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"http://ipwho.is/{ip}")
        if r.status_code == 200:
            d = r.json()
            return f"""
{C_GREEN}[IPWHO.IS]{C_RESET}
{C_YELLOW}IP: {C_CYAN}{d['ip']}
{C_YELLOW}Ülke: {C_CYAN}{d['country']} ({d['country_code']})
{C_YELLOW}Bölge: {C_CYAN}{d['region']}
{C_YELLOW}Şehir: {C_CYAN}{d['city']}
{C_YELLOW}Koordinat: {C_CYAN}{d['latitude']}, {d['longitude']}
{C_YELLOW}ISP: {C_CYAN}{d['connection']['isp']}
"""
        return f"{C_RED}Hata {r.status_code}{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu47_ip_abuse():
    ip = input(f"{C_CYAN}IP: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"https://api.abuseipdb.com/api/v2/check", params={'ipAddress':ip}, headers={'Key':'','Accept':'application/json'}, timeout=5)
        if r.status_code == 200:
            d = r.json()['data']
            return f"""
{C_GREEN}[ABUSEIPDB]{C_RESET}
{C_YELLOW}Kötü amaçlı raporu: {C_CYAN}{d['abuseConfidenceScore']}%
{C_YELLOW}Rapor sayısı: {C_CYAN}{d['totalReports']}
{C_YELLOW}Son rapor: {C_CYAN}{d['lastReportedAt']}
"""
        return f"{C_RED}Anahtar gerekli veya hata{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu48_mac_vendor():
    mac = input(f"{C_CYAN}MAC adresi (XX:XX:XX:XX:XX:XX): {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"https://api.macvendors.com/{mac}")
        if r.status_code == 200:
            return f"{C_GREEN}[MAC ÜRETİCİ]{C_RESET} {C_CYAN}{r.text.strip()}{C_RESET}"
        return f"{C_RED}Bulunamadı{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu49_bitcoin():
    addr = input(f"{C_CYAN}Bitcoin adresi: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"https://blockchain.info/rawaddr/{addr}")
        if r.status_code == 200:
            d = r.json()
            return f"""
{C_GREEN}[BITCOIN ADRES]{C_RESET}
{C_YELLOW}Toplam alınan: {C_CYAN}{d['total_received']/1e8} BTC
{C_YELLOW}Toplam gönderilen: {C_CYAN}{d['total_sent']/1e8} BTC
{C_YELLOW}Bakiye: {C_CYAN}{d['final_balance']/1e8} BTC
{C_YELLOW}İşlem sayısı: {C_CYAN}{d['n_tx']}
"""
        return f"{C_RED}Adres bulunamadı{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu50_ethereum():
    addr = input(f"{C_CYAN}Ethereum adresi: {C_RESET}")
    if not REQUESTS_OK: return "requests gerekli"
    try:
        r = requests.get(f"https://api.etherscan.io/api?module=account&action=balance&address={addr}&tag=latest&apikey=YourApiKeyToken")
        if r.status_code == 200:
            d = r.json()
            if d['status'] == '1':
                bal = int(d['result']) / 1e18
                return f"{C_GREEN}[ETH BAKİYE]{C_RESET} {C_CYAN}{bal} ETH{C_RESET}"
        return f"{C_RED}API anahtarı gerek veya hata{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu51_domain_age():
    dom = input(f"{C_CYAN}Domain: {C_RESET}")
    if not WHOIS_OK: return "whois gerekli"
    try:
        w = whois.whois(dom)
        if w.creation_date:
            if isinstance(w.creation_date, list):
                cre = w.creation_date[0]
            else:
                cre = w.creation_date
            bugun = datetime.now()
            yas = bugun - cre
            return f"{C_GREEN}[DOMAIN YAŞI]{C_RESET} {C_CYAN}{yas.days} gün (~{yas.days//365} yıl){C_RESET}"
        return f"{C_RED}Oluşturulma tarihi yok{C_RESET}"
    except Exception as e:
        return f"{C_RED}Hata: {e}{C_RESET}"

def sorgu52_story():
    tc = input(f"{C_CYAN}TC Kimlik No: {C_RESET}")
    data = story_query(tc)
    if not data:
        return f"{C_RED}Kayıt bulunamadı.{C_RESET}"
    return f"""
{C_GREEN}[HAYAT HİKAYESİ: {data['ad']} {data['soyad']}]{C_RESET}
{C_YELLOW}Doğum: {C_CYAN}{data['dogum_tarihi']} {data['dogum_yeri']}
{C_YELLOW}Meslek: {C_CYAN}{data['meslek']}
{C_YELLOW}Medeni: {C_CYAN}{data['medeni_durum']} {f"Eş: {data['es_adi']}" if data['es_adi'] else ""} {f"Çocuk: {data['cocuk_sayisi']}" if data['cocuk_sayisi'] else ""}
{C_YELLOW}Adres: {C_CYAN}{data['adres']}
{C_YELLOW}Telefon: {C_CYAN}{data['telefon']}
{C_YELLOW}E-posta: {C_CYAN}{data['email']}
{C_YELLOW}Sosyal: {C_CYAN}{data['sosyal_medya']}
{C_YELLOW}Eğitim: {C_CYAN}{data['egitim_durumu']}
{C_YELLOW}Kurum: {C_CYAN}{data['calistigi_kurum']}
{C_YELLOW}Gelir: {C_CYAN}{data['gelir_durumu']}
{C_YELLOW}Sabıka: {C_CYAN}{data['sabika']}
{C_YELLOW}Sağlık: {C_CYAN}{data['saglik_durumu']}
{C_YELLOW}Hobiler: {C_CYAN}{data['hobiler']}
{C_YELLOW}İnanç: {C_CYAN}{data['dini_inanc']}
{C_YELLOW}Siyasi: {C_CYAN}{data['siyasi_gorus']}
{C_YELLOW}Fizik: {C_CYAN}{data['boy_kilo']} | Kan: {data['kan_grubu']}
{C_YELLOW}Aile: {C_CYAN}{data['aile_ozgecmisi']}
{C_YELLOW}Önemli: {C_CYAN}{data['onemli_olaylar']}
{C_YELLOW}Son Güncelleme: {C_CYAN}{data['son_guncelleme']}
"""

def sorgu53_phone_carrier():
    return sorgu39_phone_operator()

def sorgu54_phone_geocode():
    return sorgu40_phone_location()

def sorgu55_phone_valid():
    return sorgu38_phone_detail()

menü = {
    '1': ('IP Sorgu', sorgu1_ip),
    '2': ('DNS A Kaydı', sorgu2_dns_a),
    '3': ('DNS MX Kaydı', sorgu3_dns_mx),
    '4': ('DNS NS Kaydı', sorgu4_dns_ns),
    '5': ('DNS TXT Kaydı', sorgu5_dns_txt),
    '6': ('DNS CNAME', sorgu6_dns_cname),
    '7': ('DNS PTR (Reverse)', sorgu7_dns_ptr),
    '8': ('WHOIS Domain', sorgu8_whois_domain),
    '9': ('WHOIS IP', sorgu9_whois_ip),
    '10': ('Alt Domain (crt.sh)', sorgu10_alt_domain),
    '11': ('Reverse IP (viewdns)', sorgu11_reverse_ip),
    '12': ('Port Tara (21-8443)', sorgu12_port_tara),
    '13': ('SSL Labs Analizi', sorgu13_ssl),
    '14': ('HTTP Header', sorgu14_http_header),
    '15': ('Banner Grabbing', sorgu15_banner),
    '16': ('GitHub Kullanıcı', sorgu16_github_user),
    '17': ('GitHub Repo', sorgu17_github_repo),
    '18': ('Twitter (Nitter)', sorgu18_twitter),
    '19': ('Instagram', sorgu19_instagram),
    '20': ('TikTok', sorgu20_tiktok),
    '21': ('Snapchat', sorgu21_snapchat),
    '22': ('Reddit', sorgu22_reddit),
    '23': ('YouTube', sorgu23_youtube),
    '24': ('Steam', sorgu24_steam),
    '25': ('Twitch', sorgu25_twitch),
    '26': ('Discord (ID)', sorgu26_discord),
    '27': ('Spotify', sorgu27_spotify),
    '28': ('SoundCloud', sorgu28_soundcloud),
    '29': ('Medium', sorgu29_medium),
    '30': ('dev.to', sorgu30_devto),
    '31': ('HackerNews', sorgu31_hackernews),
    '32': ('ProductHunt', sorgu32_producthunt),
    '33': ('AngelList', sorgu33_angellist),
    '34': ('Google Site Arama', sorgu34_google_site),
    '35': ('Bing Site Arama', sorgu35_bing),
    '36': ('Yandex Site Arama', sorgu36_yandex),
    '37': ('Baidu Site Arama', sorgu37_baidu),
    '38': ('Telefon Detay', sorgu38_phone_detail),
    '39': ('Telefon Operatör', sorgu39_phone_operator),
    '40': ('Telefon Konum', sorgu40_phone_location),
    '41': ('Telefon Zaman Dilimi', sorgu41_phone_timezone),
    '42': ('Telefon Hat Tipi', sorgu42_phone_type),
    '43': ('Ülke Kodu Sorgu', sorgu43_country_code),
    '44': ('E-posta Format Kontrol', sorgu44_email_validate),
    '45': ('Domain MX', sorgu45_email_mx),
    '46': ('IP Geo (ipwho.is)', sorgu46_ip_geo_alt),
    '47': ('IP Abuse (anahtar gerek)', sorgu47_ip_abuse),
    '48': ('MAC Vendor', sorgu48_mac_vendor),
    '49': ('Bitcoin Adres', sorgu49_bitcoin),
    '50': ('Ethereum (etherscan)', sorgu50_ethereum),
    '51': ('Domain Yaşı', sorgu51_domain_age),
    '52': ('HAYAT HİKAYESİ (TC)', sorgu52_story),
    '53': ('Telefon Operatör (tekrar)', sorgu53_phone_carrier),
    '54': ('Telefon Konum (tekrar)', sorgu54_phone_geocode),
    '55': ('Telefon Geçerlilik', sorgu55_phone_valid),
}

def main():
    init_db()
    while True:
        logo()
        print(f"{C_MAGENTA}{'='*60}{C_RESET}")
        print(f"{C_YELLOW}   55 SORGU HAZIR  {C_RESET}")
        print(f"{C_MAGENTA}{'='*60}{C_RESET}")
        for i in range(1,56,2):
            if i+1 <= 55:
                print(f" {C_GREEN}{i:2d}{C_RESET}. {menü[str(i)][0]:25} {C_GREEN}{i+1:2d}{C_RESET}. {menü[str(i+1)][0]}")
            else:
                print(f" {C_GREEN}{i:2d}{C_RESET}. {menü[str(i)][0]}")
        print(f"\n{C_RED}0{C_RESET}. Çıkış")
        secim = input(f"\n{C_CYAN}Seçiminiz: {C_RESET}")
        if secim == '0':
            break
        if secim in menü:
            print(f"\n{C_BLUE}[{menü[secim][0]}]{C_RESET}")
            sonuc = menü[secim][1]()
            print(sonuc)
            input(f"\n{C_YELLOW}Devam etmek için ENTER...{C_RESET}")
        else:
            print(f"{C_RED}Geçersiz seçim{C_RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C_RED}Görüşürüz.{C_RESET}")
