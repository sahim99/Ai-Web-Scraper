from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import re

def scrape_website(website):
    print("Launching Chrome Browser...")

    chrome_driver_path = "./chromedriver.exe"
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

    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    
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
    """Clean content and output structured Project/Technologies pairs for perfect LLM extraction"""
    if not body_content:
        return ""
    
    soup = BeautifulSoup(body_content, "html.parser")
    for element in soup(["script", "style", "noscript", "iframe", "embed", "object", "form"]):
        element.extract()

    # Find all project sections
    projects = []
    current_project = None
    current_techs = []
    # Look for headings or bold text as project names
    for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "b", "strong"]):
        name = tag.get_text().strip()
        if name and len(name) < 60 and any(word in name.lower() for word in ["project", "app", "dashboard", "portfolio", "work", "revamp", "chainvest", "sleepyowl", "weather", "airpods", "chatbot", "api"]):
            if current_project and current_techs:
                projects.append((current_project, list(current_techs)))
            current_project = name
            current_techs = []
            # Look for next siblings as techs
            sib = tag.find_next_sibling()
            while sib and sib.name not in ["h1", "h2", "h3", "h4", "h5", "h6", "b", "strong"]:
                sib_text = sib.get_text().strip()
                # If it's a list, add all items
                if sib.name in ["ul", "ol"]:
                    for li in sib.find_all("li"):
                        t = li.get_text().strip()
                        if t and len(t) < 50:
                            current_techs.append(t)
                elif sib_text and len(sib_text) < 50:
                    current_techs.append(sib_text)
                sib = sib.find_next_sibling()
    if current_project and current_techs:
        projects.append((current_project, list(current_techs)))

    # Fallback: Try to find project/tech pairs in paragraphs
    if not projects:
        for p in soup.find_all("p"):
            txt = p.get_text().strip()
            if ":" in txt and len(txt) < 100:
                parts = txt.split(":", 1)
                pname = parts[0].strip()
                techs = [t.strip() for t in parts[1].split(",") if t.strip()]
                if pname and techs:
                    projects.append((pname, techs))

    # Build structured output
    output = []
    for pname, techs in projects:
        output.append(f"Project: {pname}\nTechnologies: {', '.join(techs)}\n")
    if output:
        return "\n".join(output)

    # If nothing found, fallback to previous logic
    return "No projects found.\n"


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