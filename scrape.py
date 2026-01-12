from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import re

def scrape_website(website):
    print("Launching Chrome Browser...")
    
    options = webdriver.ChromeOptions()
    
    # Speed optimizations
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-images')
    options.add_argument('--disable-javascript')
    options.add_argument('--disable-css')
    options.add_argument('--disable-background-timer-throttling')
    options.add_argument('--disable-backgrounding-occluded-windows')
    options.add_argument('--disable-renderer-backgrounding')
    options.add_argument('--disable-features=TranslateUI')
    options.add_argument('--disable-ipc-flooding-protection')
    options.add_argument('--memory-pressure-off')
    options.add_argument('--max_old_space_size=4096')
    
    # Fastest page load strategy
    options.page_load_strategy = 'eager'
    
    # Check for system installed chromium (common in cloud environments)
    import shutil
    chrome_binary = shutil.which("chromium") or shutil.which("google-chrome")
    chrome_driver_binary = shutil.which("chromedriver")

    if chrome_binary:
        options.binary_location = chrome_binary

    # Use system chromedriver if available (matches package version), else use webdriver-manager
    from selenium.webdriver.chrome.service import Service as ChromeService
    
    if chrome_driver_binary:
         service = ChromeService(executable_path=chrome_driver_binary)
    else:
        from webdriver_manager.chrome import ChromeDriverManager
        service = ChromeService(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)
    
    # Set timeouts for faster failure
    driver.set_page_load_timeout(8)
    driver.implicitly_wait(2)

    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    try:
        driver.get(website)
        print("Page Loading..")
        
        # Remove fixed sleep, just wait for body
        try:
            WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except:
            pass
            
        html = driver.page_source
        return html
    except Exception as e:
        print("Error while scraping:", e)
        return ""
    finally:
        driver.quit()


def extract_body_content(html_content):
    """Extract body with better structure preservation"""
    if not html_content:
        return ""
    
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Remove only truly unnecessary elements
    for element in soup(["script", "style", "noscript", "iframe", "embed", "object"]):
        element.extract()
    
    # Keep body or main content
    body_content = soup.body
    if body_content:
        return str(body_content)
    else:
        # If no body, return the whole HTML
        return str(soup)


def clean_body_content(body_content):
    """Clean content and output structured text for perfect LLM extraction"""
    if not body_content:
        return ""
    
    soup = BeautifulSoup(body_content, "html.parser")
    for element in soup(["script", "style", "noscript", "iframe", "embed", "object", "form", "svg"]):
        element.extract()

    # Get text with separator
    text = soup.get_text(separator="\n")
    
    # Clean up whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    return text


def split_dom_content(dom_content, max_length=4000):
    """Smart content splitting that preserves structure"""
    if not dom_content:
        return []
    
    if len(dom_content) <= max_length:
        return [dom_content]
    
    # Split by paragraphs or sections to preserve structure
    chunks = []
    current_chunk = ""
    
    lines = dom_content.split('\n')
    
    for line in lines:
        # If adding this line would exceed max_length, start new chunk
        if len(current_chunk + line) > max_length and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = line + '\n'
        else:
            current_chunk += line + '\n'
    
    # Add the last chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks if chunks else [dom_content]