# scraper.py
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def scrape_product_reviews(url: str) -> list[str]:
    """
    Scrapes all comments/reviews from a given URL using a headless browser (Playwright)
    and bypassing consent/age walls.
    """
    print(f"Scraping data from: {url}")
    
    reviews = []
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
            )
            
            # 1. Add the cookie to bypass the first wall
            context.add_cookies([
                {'name': 'over18', 'value': '1', 'domain': '.reddit.com', 'path': '/'}
            ])
            
            page = context.new_page()
            
            # 2. Go to the URL and wait for it to be stable
            page.goto(url, wait_until="domcontentloaded")
            
            # 3. **--- THE NEW FIX ---**
            # Try to find the "Continue" or "Yes" button.
            # This selector looks for a button with name="yes" OR a button with the text "Continue"
            warning_button = page.locator('button[name="yes"], button:has-text("Continue")')

            try:
                # Check if the button is visible before trying to click it
                if warning_button.is_visible(timeout=3000): # Short 3s timeout
                    print("DEBUG: Content warning found. Clicking 'Continue'...")
                    
                    # Click and wait for the page to finish reloading
                    page.click('button[name="yes"], button:has-text("Continue")')
                    page.wait_for_load_state("domcontentloaded") # Wait for the new page to load
                    print("DEBUG: Page reloaded. Proceeding to scrape.")
                else:
                    print("DEBUG: No content warning found, proceeding...")
            except Exception:
                # This is OK. It just means no warning button was found.
                print("DEBUG: No content warning found (or click failed), proceeding...")

            # 4. **--- THE NEW SELECTOR ---**
            # Wait for the main comment list to appear (works on active AND archived posts)
            page.wait_for_selector('div.sitetable.nestedlisting', timeout=10000)
            
            html_content = page.content()
            context.close()
            browser.close()

        except Exception as e:
            print(f"Error during PlaylWright scraping: {e}")
            return []

    # --- This part is updated to use the new selector ---
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    print(f"DEBUG: The page title our scraper sees is: {soup.title.string}")

    # Use the same robust selector to find the comment area
    comment_area = soup.find('div', class_='sitetable nestedlisting')
    if not comment_area:
        print("DEBUG: Could not find 'sitetable nestedlisting' div. No comments to scrape.")
        return []

    # Find all comment bodies *within* that area
    comment_elements = comment_area.find_all('div', class_='md')
    
    for comment in comment_elements:
        text = comment.get_text(strip=True)
        if text:
            reviews.append(text)
            
    print(f"Found {len(reviews)} reviews.")
    return reviews