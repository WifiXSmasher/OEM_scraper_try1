from selenium import webdriver
from selenium.webdriver.common.by import By  # Used to locate elements
from selenium.webdriver.support.ui import WebDriverWait  # Waits for conditions
from selenium.webdriver.support import expected_conditions as EC  # Defines expected conditions
from bs4 import BeautifulSoup  # Parses HTML content
import time  # Used for adding delays
import data_extractor


# Function to scrape vulnerabilities from the given URI for a specific product
def scrape_vulnerabilities(URI, product):

    # List to store products that are affected by vulnerabilities
    affected_products = []

    # List to store products that are not affected (currently unused)
    not_affected_products = []

    # Initialize the Firefox WebDriver (ensure geckodriver is installed)
    driver = webdriver.Firefox()

    # List to store URIs where the product is found
    product_in_uri = []

    try:
        # Navigate to the provided URL
        driver.get(URI)

        # Create a WebDriverWait object with a timeout of 20 seconds
        wait = WebDriverWait(driver, 20)  # Max wait time is 20seconds

        # Wait until a <table> element is present on the page
        vulnerabilities_table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

        # Get the full page source and parse it using BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the first <table> element on the page
        table = soup.find("table")

        if table:  # If table exists then run the following code
            # Extract all hyperlinks from the table
            links = [a['href'] for a in table.find_all("a", href=True)]

            # Temporary list to store unique links
            link2 = []

            for link in links:
                # Add the link to link2 if it's not already in link2 and not equal to '#'
                if link not in link2 and link != '#':
                    link2.append(link)

            # Assign the unique links back to the links list
            links = link2
            print(links)# shows all the link that its going to iterate over

            # Iterate over each link and visit the page
            for link in links:
                # Open the link
                driver.get(link)

                # Wait until the <body> element is present on the page
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                # Get the new page source and parse it
                details_page = driver.page_source
                details_soup = BeautifulSoup(details_page, 'html.parser')

                # Check if the product name appears anywhere on the details page (case-insensitive)
                if product.lower() in details_soup.get_text().lower():

                    print(f"Product '{product}' found on page: {link}")
                    data_extractor.data_extractor(link, product)
                    # Add the link to the list of URIs where the product is found
                    product_in_uri.append(link)

                    try:
                        # Try to find the element with ID 'vulnerebleproducts' (ensure this ID is correct)
                        vulnerable_product = driver.find_element(By.ID, 'vulnerebleproducts')

                        # Check if the product is mentioned in the vulnerable products section
                        if product.lower() in vulnerable_product.lower().text():
                            print(f"The {vulnerable_product} was found on this {link}")

                            # Add the product to the list of affected products
                            affected_products.append(product)

                    except:
                        # If the vulnerable products section is not found, continue to the next link
                        continue

                else:
                    print(f"Product '{product}' not found on page: {link}")

                # Optional: Wait between page navigations
                time.sleep(2)

            if not links:
                print("No links found in the table.")
        else:
            print("No vulnerabilities table found.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the browser when done (cleanup)
        print(f" URIs = {product_in_uri}")
        print(f"The product in the Affected section is {affected_products}")
        driver.quit()

    # Uncomment the following line if you want the function to return the list of product URIs
    # return product_in_uri

if __name__ == "__main__":
    # Example usage of the scrape_vulnerabilities function

    # The URL of the vulnerabilities listing page
    oem_url = "https://sec.cloudapps.cisco.com/security/center/publicationListing.x"

    # The product name to search for
    scrape_vulnerabilities(oem_url, "6300 Series Embedded Services APs")
