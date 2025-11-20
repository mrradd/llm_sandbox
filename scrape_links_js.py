import sys
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin

def get_links(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            print(f"Navigating to {url}...")
            page.goto(url)
            # Wait for content to load (networkidle can be flaky on some sites)
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(2000) # Give a bit of time for hydration
            
            # Extract links
            links = page.evaluate("""
                () => {
                    return Array.from(document.querySelectorAll('a')).map(a => a.href);
                }
            """)
            
            # Filter and clean links
            unique_links = set()
            for link in links:
                if link:
                    # Playwright returns absolute URLs usually, but good to be safe
                    full_url = urljoin(url, link)
                    unique_links.add(full_url)
            
            return list(unique_links)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return []
        finally:
            browser.close()

def main():
    if len(sys.argv) < 2:
        print("Usage: python scrape_links_js.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    links = get_links(url)
    
    print(f"Found {len(links)} links:")
    for link in links:
        print(link)

if __name__ == "__main__":
    main()
