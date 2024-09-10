"""
Web Scraping Script for APG Document Hub

This script uses Selenium WebDriver to scrape document data from the APG (Austrian Power Grid) Document Hub.
It extracts document names, publication dates, document types, and legal bases from multiple pages of the site
and saves the data into a structured format (CSV file).

Key Steps:
1. Set up the Selenium WebDriver with Chrome in headless mode (no GUI).
2. Open the target webpage and scrape document information from each page.
3. Navigate through the pages by clicking the "Next" button until no more pages are available.
4. Store the scraped data in a Pandas DataFrame and save it to a CSV file for further analysis or usage.

Key Features:
- Handles pagination and scrapes data from all available pages.
- Includes error handling to ensure smooth scraping even if certain elements are missing or the page doesn't load correctly.
- Outputs the scraped data into a CSV file with columns: 'Dokumentenname', 'Veröffentlichung', 'Dokumententyp', and 'Rechtliche Grundlagen'.

Requirements:
- Selenium
- WebDriver Manager for ChromeDriver
- Pandas

Author: Ahmed Elshahed
Date: 10/09/2024
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # No GUI
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver and set up Chrome with automatic driver management
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open the target URL
driver.get("https://markt.apg.at/dokumenten-hub")
time.sleep(1)

# Initialize lists to store extracted data
doc_names, publications, doc_types, legal_bases = [], [], [], []

def scrape_page():
    """
    Function to scrape document data from the current page.
    It extracts document names, publication dates, types, and legal bases from the page.
    """
    rows = driver.find_elements(By.XPATH, "//div[contains(@class, 'document-hub-row')]")

    for row in rows:
        try:
            # Extract document name
            doc_name = row.find_element(By.XPATH, ".//div[contains(@class, 'col-xl-5')]").text.strip()
            if doc_name:
                doc_names.append(doc_name)

                # Extract details
                details = row.find_element(By.XPATH, ".//div[contains(@class, 'col-xl-7')]").text.strip()
                publication, doc_type, legal_basis = "N/A", "N/A", "N/A"

                # Parse the details
                for line in details.split("\n"):
                    if "Veröffentlichung" in line or "Start" in line:
                        publication = line.replace("Veröffentlichung:", "").replace("Start:", "").strip()
                    elif "Dokumententyp" in line:
                        doc_type = line.split(":")[-1].strip()
                    elif "Rechtliche Grundlagen" in line:
                        legal_basis = line.split(":")[-1].strip()

                publications.append(publication)
                doc_types.append(doc_type)
                legal_bases.append(legal_basis)
        except Exception as e:
            print(f"Error scraping row: {e}")

# Function to handle pagination and scrape all pages
def scrape_all_pages():
    """
    Scrape the first page, then loop through and scrape all subsequent pages
    by clicking the 'Next' button until no more pages are available.
    """

    # Scrape the first page
    scrape_page()

    while True:
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='btn-next' and @aria-disabled='false']"))
            )
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", next_button)
            time.sleep(1)  # Give time for scrolling

            next_button.click()  # Navigate to the next page
            time.sleep(1)

            scrape_page()  # Scrape the newly loaded page

        except Exception as e:
            print(f"No more pages or navigation error: {e}")
            break

# Run the scraping process
scrape_all_pages()

driver.quit()

# Create a DataFrame
df = pd.DataFrame({
    "Dokumentenname": doc_names,
    "Veröffentlichung": publications,
    "Dokumententyp": doc_types,
    "Rechtliche Grundlagen": legal_bases,
})

# Save the data in CSV File
df.to_csv("scraped_data.csv", index=False)

# Print the DataFrame to the console
print(df)