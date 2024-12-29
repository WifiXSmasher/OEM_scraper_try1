from customtkinter import *
import customtkinter
from tkinter import *
from webscraper import scrape_vulnerabilities as sv
import threading

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.geometry("815x515")
root.title("Scraper")
root.resizable(False, False)


def update_status(content):
    """Update the status text box."""
    status.configure(state=NORMAL)
    status.delete("1.0", END)
    status.insert(END, content)
    status.configure(state=DISABLED)


def update_details(data):
    """Update the details text box with formatted vulnerability data."""
    details.configure(state=NORMAL)
    details.delete("1.0", END)

    if not data:
        details.insert(END, "No vulnerabilities found.")
    else:

        details.insert(
            END,
            f"Vulnerability Details:\n"
            f"Product: {data.get('product', 'N/A')}\n"
            f"Advisory ID: {data.get('advisory_ID', 'N/A')}\n"
            f"Published Date: {data.get('published_date', 'N/A')}\n"
            f"Workarounds: {data.get('workaround', 'N/A')}\n"
            f"Cisco Bug IDs: {data.get('cisco_bug_ID', 'N/A')}\n"
            f"CVSS Score: {data.get('CVSS', 'N/A')}\n"
            f"Link: {data.get('link', 'N/A')}\n\n"
        )
    details.configure(state=DISABLED)


def task1():
    website_choice = entry.get()
    product = product_entry.get()

    if website_choice == "Enter the Website" or not product.strip():
        update_status("Please select a website and enter a product name.")
        return

    if website_choice == 'CISCO':
        website = "https://sec.cloudapps.cisco.com/security/center/publicationListing.x"
    else:
        update_status("Currently, only CISCO is supported.")
        return

    try:

        data = sv(website, product)
        if not data or "error" in data:
            update_status(f"Error occurred or no data found: {data.get('error', 'Unknown error')}")
        else:
            update_details(data)  # Update the details section
            update_status("Scraping complete!\n\nDatabase has been updated.\nThank you!")
    except Exception as e:
        update_status(f"An error occurred: {str(e)}")


def go_click():
    """Start the scraping process."""
    update_status("Scraping...")
    scraper_thread = threading.Thread(target=task1)
    scraper_thread.start()


cell_ratio = 1.4 / 2.16
rows = 10
columns = 10

for i in range(rows):
    root.rowconfigure(i, weight=1, uniform='a')

for j in range(columns):
    root.columnconfigure(j, weight=1, uniform='a')

frame = CTkFrame(root, fg_color="transparent")
frame.grid(row=1, column=0, columnspan=4, sticky="")

websites = ["Enter the Website", "CISCO"]

go = CTkButton(root,
               command=go_click,
               text="Search",
               corner_radius=10,
               hover_color="lightgreen",
               height=32,
               fg_color="green"
               )
entry = CTkOptionMenu(
    root,
    values=websites,
    font=("Arial", 12),
    fg_color="#696969",
    width=270,
    height=32
)

product_entry = CTkEntry(root,
                         placeholder_text="Enter your product name",
                         font=("Arial", 12),
                         fg_color="#696969",
                         width=275,
                         height=32,
                         )

details = CTkTextbox(root,
                     fg_color="#696969",
                     width=475,
                     height=365,
                     state=DISABLED,
                     )

status = CTkTextbox(root,
                    fg_color="#696969",
                    font=("Arial", 22),
                    state=DISABLED)

status.grid(row=1, column=7,
            columnspan=3,
            rowspan=9,
            padx=10,
            pady=50,
            sticky="nsew")

details.grid(row=3, column=0,
             columnspan=7,
             rowspan=6,
             sticky="nswe",
             padx=15)

entry.grid(row=1, column=0,
           columnspan=4,
           sticky="w",
           padx=15)

product_entry.grid(row=1, column=3,
                   sticky="e",
                   columnspan=4)

go.grid(row=1, column=8,
        sticky="ew")

root.mainloop()
