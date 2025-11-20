import sys
from playwright.sync_api import sync_playwright

def get_text(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            # Block images and other resources to save bandwidth
            page.route("**/*", lambda route: route.abort() 
                if route.request.resource_type in ["image", "media", "font", "stylesheet"] 
                else route.continue_())

            print(f"Navigating to {url}...")
            page.goto(url)
            
            # Wait for content to load
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(2000) # Give a bit of time for hydration
            
            # Extract visible text from body
            # innerText is better than textContent as it respects CSS styling (hidden elements)
            text = page.evaluate("document.body.innerText")
            return text
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return ""
        finally:
            browser.close()

def main():
    if len(sys.argv) < 2:
        print("Usage: python scrape_text_js.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    text = get_text(url)
    
    if text:
        print("--- Extracted Text ---")
        print(text)
        print("----------------------")
    else:
        print("No text found or error occurred.")

if __name__ == "__main__":
    main()
