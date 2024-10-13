from meta_ai_api import MetaAI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
ai=MetaAI()
response=ai.prompt("How is the weather")
print(response)
# Function to scrape vulnerabilities from the given URI for a specific product
def scrape_vulnerabilities(URI, product):
    # Initialize the Firefox WebDriver (ensure geckodriver is installed)
    driver = webdriver.Firefox()
    product_uri=[]
    try:
        # Navigate to the provided URL
        driver.get(URI)

        # Wait for the page to load the vulnerability table
        wait = WebDriverWait(driver, 20)  # Max wait time is 13 seconds
        vulnerabilities_table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

        # Get the full page source and parse it with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the table containing vulnerabilities
        table = soup.find("table")

        if table:
            # Extract all links in the table first, so we don't need to reload the table after each iteration
            #temp=table.find_all("a")
            #for r in temp:
               #if product.lower() in r.text.lower():
                  #print("found",r)
            links = [a['href'] for a in table.find_all("a", href=True)]
            link2=[]#temporary list to store unique links
            for link in links:
                if link not in link2:# if link exists in link2 then do not add
                    link2.append(link)

            links=link2# equating the lists
            print(links)

            # Iterate over each link and visit the page
            for link in links:
                response=ai.prompt(f"check if this product {product} is in this {link}")
                print(response)

            if not links:
                print("No links found in the table.")
        else:
            print("No vulnerabilities table found.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the browser when done (cleanup)
        print(f" URIs = {product_uri}")
        driver.quit()

    # return product_uri

if __name__ == "__main__":
    # Example usage of the scrape_vulnerabilities function
    oem_url = "https://sec.cloudapps.cisco.com/security/center/publicationListing.x"
    scrape_vulnerabilities(oem_url, "Cisco NDFC")