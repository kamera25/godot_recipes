import os
import urllib.request
from html.parser import HTMLParser

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    self.links.append(value)

def check_url(url):
    """Checks if a URL is reachable (not 404)."""
    try:
        # Use HEAD request if possible, then GET
        req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.getcode()
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return None

def check_local_link(base_path, link_path):
    """Checks if a local link exists on the filesystem."""
    # Remove fragments and queries
    link_path = link_path.split('#')[0].split('?')[0]
    if not link_path:
        return True
    
    # Resolve relative path
    abs_path = os.path.normpath(os.path.join(os.path.dirname(base_path), link_path))
    
    # If it's a directory, check for index.html
    if os.path.isdir(abs_path):
        return os.path.exists(os.path.join(abs_path, 'index.html'))
    
    # Standard file check
    return os.path.exists(abs_path)

def main(docs_dir):
    results = []
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                print(f"Checking: {file_path}")
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                parser = LinkParser()
                parser.feed(content)
                
                for link in parser.links:
                    # Skip if link is None or empty
                    if not link:
                        continue
                    
                    # Skip anchors within the same page
                    if link.startswith('#'):
                        continue
                    
                    # Handle external links
                    if link.startswith(('http://', 'https://')):
                        code = check_url(link)
                        if code == 404:
                            results.append((file_path, link))
                    
                    # Handle local links (experimental)
                    elif not link.startswith(('mailto:', 'tel:', 'javascript:')):
                        if not check_local_link(file_path, link):
                            results.append((file_path, link))
    
    print("\n--- 404 Links Found ---")
    if not results:
        print("No 404 links found.")
    for src, target in results:
        print(f"Source: {src}")
        print(f"  Target: {target}")
        print("-" * 20)

if __name__ == "__main__":
    DOCS_ROOT = os.path.abspath("./docs")
    if not os.path.exists(DOCS_ROOT):
        print(f"Error: Directory {DOCS_ROOT} not found.")
    else:
        main(DOCS_ROOT)
