import requests
import re
from concurrent.futures import ThreadPoolExecutor
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def detect_wordpress_cms(url):
    base_url = url.rstrip('/')
    endpoints = [
        base_url,
        f"{base_url}/wp-admin/install.php",
        f"{base_url}/feed/",
        f"{base_url}/?feed=rss2"
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'
    }

    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, headers=headers, allow_redirects=True, verify=False)
            if response.status_code == 200:
                if has_wordpress_signature(response.text):
                    return (url, True)
        except requests.exceptions.RequestException:
            pass
    
    return (url, False)

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

# Read the list of URLs from list.txt file
with open('list.txt', 'r') as file:
    urls = file.read().splitlines()

def worker(url):
    result = detect_wordpress_cms(url)
    if result[1]:
        return f"WordPress CMS detected. URL: {result[0]}"
    else:
        return f"Not a WordPress CMS. URL: {result[0]}"

# Set the maximum number of threads
max_threads = 50

# Create a ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=max_threads) as executor:
    results = executor.map(worker, urls)

# Save the results to wordpress.txt
with open('wordpress.txt', 'w') as file:
    for result in results:
        if result.startswith("WordPress CMS"):
            file.write(result.split("URL: ")[1] + '\n')

# Print the results
for result in results:
    print(result)

print("WordPress CMS detection completed.")
