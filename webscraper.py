from selenium import webdriver
from selenium.webdriver.common.by import By  # Used to locate elements
from selenium.webdriver.support.ui import WebDriverWait  # Waits for conditions
from selenium.webdriver.support import expected_conditions as EC  # Defines expected conditions
from bs4 import BeautifulSoup  # Parses HTML content
import time  # Used for adding delays
from data_extractor import Data_extractor as DE


# Function to scrape vulnerabilities from the given URI for a specific product
def scrape_vulnerabilities(URI, product):
    affected_products = []

    # list to store products that are not affected (currently unused)
    not_affected_products = []

    driver = webdriver.Firefox()

    product_in_uri = []

    try:
        driver.get(URI)
        wait = WebDriverWait(driver, 60)
        vulnerabilities_table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find("table")
        # wait_2 = WebDriverWait(driver,10)
        if table:
            links = [a['href'] for a in table.find_all("a", href=True)]
            link2 = []
            results = []
            for link in links:
                if link not in link2 and link != '#':
                    link2.append(link)

            links = link2
            print(links)
            if not links:
                print(f"links:{links}\nlinks2:{link2}")
                print("No links found in the table.")
            else:
                for link in links:
                    driver.get(link)
                    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                    details_page = driver.page_source
                    details_soup = BeautifulSoup(details_page, 'html.parser')

                    if product.lower() in details_soup.get_text().lower():
                        print(f"Product '{product}' found on page: {link}")
                        # DE.extract(link, product)
                        data = DE.extract(link, product)
                        print(f"THIS IS THE EXTRACTED DATA:\n {data}")
                        if data:
                            # results.append(data)
                            # return {"success": True, "data": results}
                            return data

                        product_in_uri.append(link)

                        try:
                            vulnerable_product = driver.find_element(By.ID, 'vulnerebleproducts')
                            if product.lower() in vulnerable_product.lower().text():
                                print(f"The {vulnerable_product} was found on this {link}")
                                affected_products.append(product)

                        except:
                            continue

                    else:
                        print(f"Product '{product}' not found on page: {link}")

                    # Optional: Wait between page navigations
                    # time.sleep(2)

        else:
            return {"success": False, "error": "No vulnerabilities table found."}

    except Exception as e:
        print(f"the scrper only didnt work")
        return {"success": False, "error": str(e)}

    finally:
        # print(f" URIs = {product_in_uri}")
        # print(f"The product in the Affected section is {affected_products}")
        driver.quit()


if __name__ == "__main__":

    # The URL of the vulnerabilities listing page
    oem_url = "https://sec.cloudapps.cisco.com/security/center/publicationListing.x"

    # The product name to search for
    scrape_vulnerabilities(oem_url, "MDS 9000 Series Multilayer Switches ")




# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# from selenium import webdriver
# from selenium.webdriver.common.by import By  # Used to locate elements
# from selenium.webdriver.support.ui import WebDriverWait  # Waits for conditions
# from selenium.webdriver.support import expected_conditions as EC  # Defines expected conditions
# from bs4 import BeautifulSoup  # Parses HTML content
# import time  # Used for adding delays
# from data_extractor import Data_extractor as DE
#
#
# # Function to scrape vulnerabilities from the given URI for a specific product
# def scrape_vulnerabilities(URI, product):
#
#     affected_products = []
#
#     # list to store products that are not affected (currently unused)
#     not_affected_products = []
#
#     driver = webdriver.Firefox()
#
#     # list to store URIs where the product is found
#     product_in_uri = []
#
#     try:
#
#         driver.get(URI)
#         wait = WebDriverWait(driver, 30)
#
#         # wait until a <table> element is present on the page
#         vulnerabilities_table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
#
#         # get the full page source and parse it using BeautifulSoup
#         page_source = driver.page_source
#         soup = BeautifulSoup(page_source, 'html.parser')
#
#         # find the first <table> element on the page
#         table = soup.find("table")
#
#         if table:
#             #extract all hyperlinks from the table
#             links = [a['href'] for a in table.find_all("a", href=True)]
#
#             # temp list to store unique links
#             link2 = []
#
#             for link in links:
#                 # add the link to link2 if it's not already in link2 and not equal to '#'
#                 if link not in link2 and link != '#':
#                     link2.append(link)
#
#             # Assign the unique links back to the links list
#             links = link2
#             print(links)  # shows all the link that its going to iterate over
#
#             # iterate over each link and visit the page
#             for link in links:
#                 # Open the link
#                 driver.get(link)
#
#                 # Wait until the <body> element is present on the page
#                 WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
#
#                 # Get the new page source and parse it
#                 details_page = driver.page_source
#                 details_soup = BeautifulSoup(details_page, 'html.parser')
#
#                 # Check if the product name appears anywhere on the details page (case-insensitive)
#                 if product.lower() in details_soup.get_text().lower():
#
#                     print(f"Product '{product}' found on page: {link}")
#                     DE.extract(link, product)
#                     # Add the link to the list of URIs where the product is found
#                     product_in_uri.append(link)
#
#                     try:
#                         # Try to find the element with ID 'vulnerebleproducts' (ensure this ID is correct)
#                         vulnerable_product = driver.find_element(By.ID, 'vulnerebleproducts')
#
#                         # Check if the product is mentioned in the vulnerable products section
#                         if product.lower() in vulnerable_product.lower().text():
#                             print(f"The {vulnerable_product} was found on this {link}")
#
#                             # Add the product to the list of affected products
#                             affected_products.append(product)
#
#                     except:
#                         # If the vulnerable products section is not found, continue to the next link
#                         continue
#
#                 else:
#                     print(f"Product '{product}' not found on page: {link}")
#
#                 # Optional: Wait between page navigations
#                 time.sleep(2)
#
#             if not links:
#                 print("No links found in the table.")
#         else:
#             print("No vulnerabilities table found.")
#
#     except Exception as e:
#         print(f"An error occurred: {e}")
#
#     finally:
#         # Close the browser when done (cleanup)
#         print(f" URIs = {product_in_uri}")
#         print(f"The product in the Affected section is {affected_products}")
#         driver.quit()
#
#     # Uncomment the following line if you want the function to return the list of product URIs
#     # return product_in_uri
#
#
# if __name__ == "__main__":
#     # Example usage of the scrape_vulnerabilities function
#
#     # The URL of the vulnerabilities listing page
#     oem_url = "https://sec.cloudapps.cisco.com/security/center/publicationListing.x"
#
#     # The product name to search for
#     scrape_vulnerabilities(oem_url, "MDS 9000 Series Multilayer Switches ")