This is a project done by me

This project is a Python-based web scraper designed to detect and analyze vulnerabilities in OEM products. It comprises several scripts, each serving a distinct purpose:
    
    1.webscraper.py: This script searches for all the links in the provided website link and looks for mentions of the product.
            i it uses BeautifulSoup and Selenium to do so.
    
    2.data_extractor.py: When a product is found on a page, this script fetches all the details about the vulnerability found.
            i. The script is generalized as much as possible using XPath expressions to ensure reliable extraction.

    3.database.py: This script updates the database:
            i. If the data for a product is already scraped, it avoids updating to prevent duplication.
            ii. Users can view the database contents.
    
    4.message.py: This script is invoked when the data_extractor.py script completes its task, and valid data is obtained.
            i. It sends an email notification to the user, providing details of the newly found vulnerabilities.
                    
    5.scraper_GUI.py: The GUI is built using Tkinter and CustomTkinter:
            i. It uses the grid method for structure.
            ii. A status box and a details box display the scraping results in a non-editable format.
            iii. The GUI includes several additional features(i will be updating it after some time).
    
    6.vulnerabilities.db: This is the database file that securely stores all the collected vulnerability data.          

I have rarely use LLM models for this script so there can be some buggy and unclean code  ( which i will fix as i find them)
