# scraper.py
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def scrape_product_reviews(url: str) -> list[str]:
    """
    Scrapes all comments/reviews from a given URL using a clean headless browser.
    """
    print(f"Scraping data from: {url}")
    
    reviews = []
    
    with sync_playwright() as p:
        try:
            # 1. Launch browser and create context
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                # Use a specific, common User-Agent
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
            )
            
            # 2. Add the over18 cookie (critical for age gates)
            context.add_cookies([
                {'name': 'over18', 'value': '1', 'domain': '.reddit.com', 'path': '/'}
            ])
            
            page = context.new_page()
            
            page.goto(url, wait_until="domcontentloaded")
            
            # 3. Handle "Are You Sure" Warning (Content Wall Bypass)
            warning_button = page.locator('button[name="yes"], button:has-text("Continue")')

            try:
                if warning_button.is_visible(timeout=3000):
                    print("DEBUG: Content warning found. Clicking 'Continue'...")
                    page.click('button[name="yes"], button:has-text("Continue")')
                    page.wait_for_load_state("domcontentloaded") 
                    print("DEBUG: Page reloaded. Proceeding to scrape.")
                else:
                    print("DEBUG: No content warning found, proceeding...")
            except Exception:
                # This is OK. It just means the button wasn't there.
                pass 

            # 4. Wait for the main comment list to appear
            page.wait_for_selector('div.sitetable.nestedlisting', timeout=10000)
            
            # 5. Get the final HTML
            html_content = page.content()
            context.close()
            browser.close()

        except Exception as e:
            # This will now catch the error if detection fails, and return 0 reviews
            print(f"Error during Playwright scraping: {e}")
            return []

    # 6. Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    print(f"DEBUG: The page title our scraper sees is: {soup.title.string}")

    comment_area = soup.find('div', class_='sitetable nestedlisting')
    if not comment_area:
        print("DEBUG: Could not find 'sitetable nestedlisting' div. No comments to scrape.")
        return []

    comment_elements = comment_area.find_all('div', class_='md')
    
    for comment in comment_elements:
        text = comment.get_text(strip=True)
        if text:
            reviews.append(text)
            
    print(f"Found {len(reviews)} reviews.")
    return reviews