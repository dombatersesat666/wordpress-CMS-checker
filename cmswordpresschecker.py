import requests
import re
import concurrent.futures

def detect_wordpress_cms(url):
    base_url = url.rstrip('/')
    endpoints = [
        base_url,
        f"{base_url}/wp-admin/install.php",
        f"{base_url}/feed/",
        f"{base_url}/?feed=rss2"
    ]

    for endpoint in endpoints:
        response = requests.get(endpoint, allow_redirects=True)
        if response.status_code == 200:
            if has_wordpress_signature(response.text):
                return True
    
    return False

def has_wordpress_signature(content):
    signatures = [
        r'<generator>https?:\/\/wordpress\.org.*</generator>',
        r'wp-login.php',
        r'\/wp-content/themes\/',
        r'\/wp-includes\/',
        r'name="generator" content="wordpress',
        r'<link[^>]+s\d+\.wp\.com',
        r'<!-- This site is optimized with the Yoast (?:WordPress )?SEO plugin v([\d.]+) -',
        r'<!--[^>]+WP-Super-Cache'
    ]

    for signature in signatures:
        if re.search(signature, content):
            return True
    
    return False

# Baca daftar URL dari file list.txt
with open('list.txt', 'r') as file:
    urls = file.read().splitlines()

# Fungsi worker untuk setiap thread
def worker(url):
    if detect_wordpress_cms(url):
        with open('wordpress.txt', 'a') as file:
            file.write(f"{url}\n")
        print(f"WordPress CMS detected. URL: {url}")
    else:
        print(f"Not a WordPress CMS. URL: {url}")

# Lakukan deteksi CMS WordPress dengan menggunakan thread
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    executor.map(worker, urls)

print("Deteksi CMS WordPress selesai.")
