import re
import requests
from multiprocessing.dummy import Pool as ThreadPool
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def check_wordpress(domain):
    urls = [
        f"http://{domain}",
        f"http://{domain}/wp-admin/install.php",
        f"http://{domain}/feed/"
    ]
    for url in urls:
        try:
            response = requests.get(url, allow_redirects=True, verify=False, timeout=5)
            if response.status_code == 200:
                content = response.text
                if re.search(r'<generator>https?:\/\/wordpress\.org.*</generator>', content) or \
                        re.search(r'wp-login.php', content) or \
                        re.search(r'\/wp-content/themes\/', content) or \
                        re.search(r'\/wp-includes\/', content) or \
                        re.search(r'name="generator" content="wordpress', content) or \
                        re.search(r'<link[^>]+s\d+\.wp\.com', content) or \
                        re.search(r'<!-- This site is optimized with the Yoast (?:WordPress )?SEO plugin v([\d.]+) -', content) or \
                        re.search(r'<!--[^>]+WP-Super-Cache', content):
                    print(f"Domain WordPress ditemukan: {domain}")
                    with open("wordpress.txt", "a") as file:
                        file.write(f"{domain}\n")
                    return domain
        except (requests.exceptions.RequestException, requests.exceptions.Timeout):
            pass
    return None

if __name__ == "__main__":
    filename = input("Masukkan nama file: ")
    num_threads = int(input("Masukkan jumlah thread: "))

    with open(filename, "r", errors='ignore') as file:
        domains = file.read().splitlines()

    pool = ThreadPool(num_threads)
    results = pool.map(check_wordpress, domains)
    pool.close()
    pool.join()

    wordpress_domains = [domain for domain in results if domain is not None]

    
    print("Pengecekan domain WordPress telah selesai.")
