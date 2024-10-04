from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_vulnerabilities(oem_url):
    driver = webdriver.Chrome()

    driver.get(oem_url)

    try:
        # Wait for the vulnerability list to load
        wait = WebDriverWait(driver, 10)

        # Find the elements in the <table>
        vulnerabilities = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "table")))

        # Print the text of each vulnerability entry
        if vulnerabilities:
            doc = driver.page_source
            soup = BeautifulSoup(doc, 'html.parser')

            # Find all <tr> elements within the table
            rows = soup.find_all("tr")

            # Iterate through each row to extract <td> elements
            unique=[]
            for row in rows:
                # Get all <td> elements in the current row
                cells = row.find_all("td")
                # Extract and print the text from each <td>
                for cell in cells:
                    cell_text = cell.get_text(strip=True)
                    if cell_text: # Only print non-empty text
                        print(cell_text)
        else:
            print("No vulnerabilities found.")
    finally:
        driver.quit()

# Example usage
oem_url = "https://sec.cloudapps.cisco.com/security/center/publicationListing.x"  # site URL for all the vulnerabilities
scrape_vulnerabilities(oem_url)