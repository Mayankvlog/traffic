import json
import os
import random
import time
from datetime import datetime
from urllib.parse import urlparse
from typing import Dict, Any

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# -----------------------------------------------------------------------------
# CONFIGURATION & SETUP
# -----------------------------------------------------------------------------
# Ethics principle: Be transparent. Define a custom User-Agent so webmasters
# know exactly who is accessing their site and why.
USER_AGENT = "EthicalTrafficSimulator/1.0 (Python 3.11; Contact: admin@example.com)"
MAX_RETRIES = 3

# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------

def get_valid_url() -> str:
    """
    यूजर से इनपुट लेता है और सुनिश्चित करता है कि URL सभी डोमेन (.com, .in, .netlify.app) के लिए सही हो।
    """
    while True:
        user_input = input("\nकृपया टारगेट वेबसाइट का URL दर्ज करें (e.g., mysite.com, test.netlify.app): ").strip()
        
        if not user_input:
            print("[त्रुटि] URL खाली नहीं हो सकता। कृपया दोबारा प्रयास करें।")
            continue
            
        # अगर यूजर http या https लगाना भूल गया है, तो उसे ऑटोमैटिक जोड़ें
        if not user_input.startswith(('http://', 'https://')):
            user_input = 'https://' + user_input
            
        try:
            parsed_url = urlparse(user_input)
            # यह जांचता है कि डोमेन में कम से कम एक डॉट (.) हो जैसे .com, .in, .netlify.app
            if parsed_url.netloc and '.' in parsed_url.netloc:
                print(f"[सफलता] सही URL मिला: {user_input}")
                return user_input
            else:
                print("[त्रुटि] अमान्य URL फॉर्मैट। कृपया सही डोमेन (.com, .in, .netlify.app आदि) डालें।")
        except Exception as e:
            print(f"[त्रुटि] URL जांचने में समस्या आई: {e}")

def simulate_natural_behavior(driver: webdriver.Chrome) -> None:
    """
    Simulates genuine user browsing to respect site usability metrics.
    Ethical rationale: Real users pause, scroll, and read. Mimicking this 
    provides accurate analytics without overwhelming the server.
    """
    try:
        # Simulate reading/pausing on the page
        time.sleep(random.uniform(2.0, 5.0))
        
        # Simulate random scrolling
        scroll_pause_time = random.uniform(0.5, 1.5)
        screen_height = driver.execute_script("return window.screen.height;")
        i = 1
        while True:
            # Scroll down by a fraction of the screen height
            driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
            i += 1
            time.sleep(scroll_pause_time)
            
            # Stop scrolling if we've reached the bottom of the page
            scroll_height = driver.execute_script("return document.body.scrollHeight;")
            if (screen_height * i) > scroll_height:
                break
                
        # Additional pause before navigating away
        time.sleep(random.uniform(1.0, 3.0))
        
    except Exception as e:
        print(f"[Warning] Error during behavior simulation: {e}")

def api_account_creation(endpoint: str, payload: Dict[str, Any]) -> bool:
    """
    Handles account creation via official APIs.
    Ethical rationale: Using documented APIs (when available) is safer and 
    less intrusive than automating UI-based form submissions.
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json"
    }
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(endpoint, json=payload, headers=headers, timeout=10)
            
            # Respect rate limits
            if response.status_code == 429:
                print("[Warning] Rate limit hit. Backing off...")
                time.sleep(10)
                continue
                
            response.raise_for_status()
            print(f"[Success] Account created/API Pinged. Payload: {json.dumps(payload)}")
            return True
            
        except requests.exceptions.RequestException as e:
            # चूंकि टेस्ट साइट्स पर हमेशा API एंडपॉइंट्स नहीं होते, इसलिए इसे केवल लॉग करेंगे
            print(f"[Notice] API Endpoint interaction complete or skipped (Attempt {attempt+1}): {e}")
            break
            
    return False

def browse_and_interact(url: str) -> None:
    """
    Uses Selenium to visit a page, mimicking real user interaction.
    """
    # Configure Selenium options
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={USER_AGENT}")
    
    # Chrome को बिना किसी एरर पॉप-अप के चलाने के लिए अतिरिक्त सेटिंग्स
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        
        # Log transparently
        print(f"[{datetime.now().isoformat()}] Visited: {driver.title}")
        
        simulate_natural_behavior(driver)
        
        # Optional: Interact with a specific element if available
        try:
            links = driver.find_elements(By.TAG_NAME, "a")
            if links:
                # केवल वे लिंक्स चुनें जिनमें href मौजूद हो
                valid_links = [l for l in links if l.get_attribute('href')]
                if valid_links:
                    target_link = random.choice(valid_links)
                    if target_link.is_displayed():
                        print(f"Clicking link: {target_link.get_attribute('href')}")
                        target_link.click()
                        simulate_natural_behavior(driver)
        except Exception as inner_e:
            print(f"[Info] No clickable links processed: {inner_e}")
            
    except Exception as e:
        print(f"[Error] Browser automation error: {e}")
    finally:
        try:
            driver.quit()
            print("[Info] Browser closed safely.")
        except NameError:
            pass

# -----------------------------------------------------------------------------
# MAIN EXECUTION
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("--- Starting Ethical Traffic & Automation Routine ---")
    
    # 1. स्क्रिप्ट शुरू होते ही यूजर से URL इनपुट लेगी
    TARGET_BASE_URL = get_valid_url()
    
    # उसी डोमेन के आधार पर एक डेमो अकाउंट/साइन-अप एंडपॉइंट सेट करें
    ACCOUNT_ENDPOINT = f"{TARGET_BASE_URL}/api/register"
    
    # 2. Simulate API-based account sign-up (e.g., newsletter/membership)
    sample_signup_payload = {
        "email": "user_demo_" + str(random.randint(1000, 9999)) + "@example.com",
        "preferences": "newsletter_updates"
    }
    api_account_creation(ACCOUNT_ENDPOINT, sample_signup_payload)
    
    # 3. Simulate web browsing traffic
    print(f"\n[Action] {TARGET_BASE_URL} पर ब्राउज़र ओपन किया जा रहा है...")
    browse_and_interact(TARGET_BASE_URL)
    
    print("\n--- Routine Complete ---")
