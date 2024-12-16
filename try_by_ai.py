import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Function to scrape vulnerabilities from the given URI for a specific product
def scrape_page(driver, link, product, product_in_uri):
    try:
        # Open the link
        driver.get(link)

        # Wait for the new page to load
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Get the new page source and parse it
        details_page = driver.page_source
        details_soup = BeautifulSoup(details_page, 'html.parser')

        # Check if the product name appears on the details page
        if product.lower() in details_soup.get_text().lower():
            print(f"Product '{product}' found on page: {link}")
            product_in_uri.append(link)
        else:
            print(f"Product '{product}' not found on page: {link}")

    except Exception as e:
        print(f"Error processing link {link}: {e}")

# Main function to handle threading
def scrape_vulnerabilities(URI, product):
    driver = webdriver.Firefox()
    product_in_uri = []
    try:
        # Navigate to the provided URL
        driver.get(URI)

        # Wait for the page to load the vulnerability table
        wait = WebDriverWait(driver, 20)
        vulnerabilities_table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

        # Get the full page source and parse it with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the table containing vulnerabilities
        table = soup.find("table")
        if table:
            links = [a['href'] for a in table.find_all("a", href=True)]
            link2 = [link for link in links if link != '#']
            print(link2)

            threads = []
            for link in link2:
                thread = threading.Thread(target=scrape_page, args=(driver, link, product, product_in_uri))
                thread.start()
                threads.append(thread)

            # Wait for all threads to complete
            for thread in threads:
                thread.join()

        else:
            print("No vulnerabilities table found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Cleanup
        print(f"URIs: {product_in_uri}")
        driver.quit()

if __name__ == "__main__":
    oem_url = "https://sec.cloudapps.cisco.com/security/center/publicationListing.x"
    scrape_vulnerabilities(oem_url, "RV340 Dual WAN")
