from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_vulnerabilities(oem_url):
    driver = webdriver.Chrome()

    driver.get(oem_url)

    try:
        # Wait for the vulnerability list to load
        wait = WebDriverWait(driver, 10)

        # Try to find elements
        vulnerabilities = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ng-binding")))

        # Print the text of each vulnerability entry
        if vulnerabilities:
            for vuln in vulnerabilities:
                print(vuln.text)  # Extract and print the text from each element
        else:
            print("No vulnerabilities found.")

    finally:
        driver.quit()


oem_url = "https://sec.cloudapps.cisco.com/security/center/publicationListing.x"
scrape_vulnerabilities(oem_url)
