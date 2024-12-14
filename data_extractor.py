import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC

"""
1. go to the link 
2. extract the data of 
    i.) Advisory ID:
    ii.) First Published:
    iii.) Last Updated:
    iv.) Workarounds:
    V.) Cisco Bug IDs:
    Vi.) CVSS Score:

"""


def data_extractor(link, product):
    driver = webdriver.Firefox()

    try:
        driver.get(link)  #get the webdriver

        wait = WebDriverWait(driver, 5)  #wait for the webdriver for 5 sec

        #for advisory_id
        advisory_id = wait.until(EC.presence_of_element_located((By.ID, "divpubidvalue"))).text.strip()

        #for first published
        parent_element = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.ID, "ud-published"))
        )
        content_element = parent_element.find_element(By.CLASS_NAME, "divLabelContent")
        published_date = content_element.text

        #ud-last-updated
        try:
            parent_element = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.ID, "ud-last-updated"))
            )
            content_element = parent_element.find_element(By.CLASS_NAME, "divLabelContent")
            last_published_date = content_element.text

        except:
            print(f"last published date not found")

        # #for workaround
        # parent_element = WebDriverWait(driver, 2).until(
        #     EC.presence_of_element_located((By.ID, "advisorycontentheader"))
        # )
        # content_element = parent_element.find_element((By.CLASS_NAME, "divPaddingTen pubheaderrow"))
        # workaround = content_element.find_element((By.CLASS_NAME,"divLabelContent"))
        # workaround = workaround.text

        # #ud-ddts
        # parent_element = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.ID, "ud-last-updated"))
        # )
        # content_element = parent_element.find_element(By.CLASS_NAME, "divLabelContent")
        # last_published_date = content_element.text

        print(f"the Advisory ID is : {advisory_id}")
        print(f"the first publish date was : {published_date}")
        # print(f"workarounds: {workaround}")

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        driver.quit()
        return


if __name__ == "__main__":
    link = "https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-cucm-xss-SVCkMMW"
    product = "6300 Series Embedded Services APs"
    data_extractor(link, product)
