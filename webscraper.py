from selenium import webdriver
from selenium.webdriver.common.by import By  #  to locate elements
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  # defines expected conditions
from bs4 import BeautifulSoup  # for parsing HTML content
import time  
from data_extractor import Data_extractor as DE



def scrape_vulnerabilities(URI, product):
    affected_products = []

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

                    # optional: wait between page navigations
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
# from selenium.webdriver.common.by import By 
# from selenium.webdriver.support.ui import WebDriverWait 
# from selenium.webdriver.support import expected_conditions as EC  
# from bs4 import BeautifulSoup 
# import time  
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
#        
#         vulnerabilities_table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
#
#      
#         page_source = driver.page_source
#         soup = BeautifulSoup(page_source, 'html.parser')
#
#       
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
#          
#             links = link2
#             print(links)  # shows all the link that its going to iterate over
#
#        
#             for link in links:
#                 # Open the link
#                 driver.get(link)
#
#               
#                 WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
#
#                 details_page = driver.page_source
#                 details_soup = BeautifulSoup(details_page, 'html.parser')
#
#                 if product.lower() in details_soup.get_text().lower():
#
#                     print(f"Product '{product}' found on page: {link}")
#                     DE.extract(link, product)
#                     product_in_uri.append(link)
#
#                     try:
#                         vulnerable_product = driver.find_element(By.ID, 'vulnerebleproducts')
#                         if product.lower() in vulnerable_product.lower().text():
#                             print(f"The {vulnerable_product} was found on this {link}")
#
#                             affected_products.append(product)
#
#                     except:
#                         # If the vulnerable products section is not found, continue to the next link
#                         continue
#
#                 else:
#                     print(f"Product '{product}' not found on page: {link}")
#
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
#         print(f" URIs = {product_in_uri}")
#         print(f"The product in the Affected section is {affected_products}")
#         driver.quit()
#
#
#
# if __name__ == "__main__":
#
#     # the URL of the vulnerabilities listing page
#     oem_url = "https://sec.cloudapps.cisco.com/security/center/publicationListing.x"
#
#     # the product name to search for
#     scrape_vulnerabilities(oem_url, "MDS 9000 Series Multilayer Switches ")
