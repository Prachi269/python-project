from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Replace with your own ChromeDriver path
CHROME_DRIVER_PATH = "C:/path/to/chromedriver.exe"  # 🔁 Replace this!

# Get user input
mobile_number = input("Enter the mobile number: ")

# Setup Chrome options
options = Options()
options.add_argument("--headless")  # Optional: remove to see the browser
options.add_argument("--disable-blink-features=AutomationControlled")  # For stealth
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the website
    driver.get("https://www.findandtrace.com/trace-mobile-number-location")

    # Input mobile number
    mobile_input = driver.find_element(By.NAME, "mobilenumber")
    mobile_input.send_keys(mobile_number)

    # Click the trace button
    submit_button = driver.find_element(By.ID, "mobsearch")
    submit_button.click()

    # Wait for page to load results
    time.sleep(3)

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    tables = soup.find_all("table", class_="shop_table")

    # Extract and display data
    if len(tables) >= 2:
        print("\n📍 Trace Result:")
        for table in tables:
            for row in table.find_all("tr"):
                th = row.find("th")
                td = row.find("td")
                if th and td:
                    print(f"{th.text.strip()}: {td.text.strip()}")
    else:
        print("❌ Failed to extract mobile info. Site structure may have changed.")

finally:
    driver.quit()
