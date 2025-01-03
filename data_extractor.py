import re
import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from database import DB
from message import Mail


class Data_extractor:
    """
    1. make a database and trans
    """

    @staticmethod
    def extract(link, product):
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
        driver = webdriver.Firefox()

        try:
            driver.get(link)  #get the webdriver

            wait = WebDriverWait(driver, 5)  #wait for the webdriver for 5 sec

            #for advisory_id
            advisory_id = wait.until(EC.presence_of_element_located((By.ID, "divpubidvalue"))).text.strip()

            #for first published
            parent_element = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "ud-published")))
            content_element = parent_element.find_element(By.CLASS_NAME, "divLabelContent")
            published_date = content_element.text

            #ud-last-updated
            # try:
            #     parent_element = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "ud-last-updated")))
            #     content_element = parent_element.find_element(By.CLASS_NAME, "divLabelContent")
            #     last_published_date = content_element.text
            # except:
            #     print(f"last published date not found")

            # for workaround element
            workarounds_element = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(text(), 'Workarounds:')]/following-sibling::div")))
            workarounds = workarounds_element.text

            #for cisco bug id
            cisco_bug_id = WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located(
                (By.XPATH, "//div[contains(text(),'Cisco Bug IDs:')]/following-sibling::div//a")))
            cisco_bug_id = [id.text for id in cisco_bug_id if id.text != '']

            #for CVSS score
            cvss = [re.search(r'\d+\.\d+', score.text).group(0) for score in WebDriverWait(driver, 1).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//div[contains(text(), 'CVSS Score:')]//following-sibling::div//a")))]
            cvss = cvss[0]

            # print statements for debugging
            # print(f"the Advisory ID is : {advisory_id}")
            # print(f"the first publish date was : {published_date}")
            # # print(f"the last date was: {last_published_date}")
            # print("Workarounds:", workarounds)
            # print(f"Cisco Bug IDs:{cisco_bug_id}")
            # print(f"CVSS Score:{cvss}")
            data = {
                "product": product,
                "advisory_ID": advisory_id,
                "published_date": published_date,
                "workaround": workarounds,
                "cisco_bug_ID": cisco_bug_id,
                "CVSS": cvss,
                "link": link
            }
            print(data)
            DB.append("vulnerabilities.db", data, " properties")
            return data
        except Exception as e:
            print(f"an error occurred during data extraction of link:{link} : {e}")
            return {"error": str(e)}

        finally:
            driver.quit()
            Mail.email(product, link, data)


        # return {
        #     "advisory_id": advisory_id,
        #     "published_date": published_date,
        #     "workarounds": workarounds,
        #     "cisco_bug_id": cisco_bug_id,
        #     "cvss": cvss
        # }

# for testin the oblect
# if __name__ == "__main__":
#         link = "https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-cucm-xss-SVCkMMW"
#         #https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-ap-dos-capwap-DDMCZS4m
#         #https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-cucm-xss-SVCkMMW
#         product = "6300 Series Embedded Services APs"
#         data_extractor(link, product)
