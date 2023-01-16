from selenium import webdriver
import time
import bs4 as bs
import pandas as pd
import yagmail

##### Settings #####
store_list = [
    ["Mcalister Square","https://www.publix.com/locations/602-mcalister-square"],
    ["Center Point","https://www.publix.com/locations/205-center-point"],
    ["McBee Station","https://www.publix.com/locations/1148-mcbee-station"]
    ]
GMAIL_username = 'XXXXXXXXX@gmail.com'
GMAIL_password = 'XXXXXXXXX'
target_email = 'XXXXXXXXX@gmail.com'
deal_dict = {} # Create empty dictionary to store deals by store
web_driver_path = r'C:\Users\XXXXXXXXXXXXXXXXXXXX\chromedriver.exe'

##### XPath Variables #####
loadmore = '//*[@id="main"]/div[4]/div/div[2]/div[2]/div[4]/button/span'

shop_at_this_store = '//*[@id="main"]/div[3]/div[1]/button'

# Create selenium webdriver
browser = webdriver.Chrome(executable_path = web_driver_path)


# Function to click on xpath elements
def clickButton(path):
    try:
        browser.find_element_by_xpath(path).click()
        pass
    except Exception:
        time.sleep(1.0)
        clickButton(path)


# Get the deals from each store and assign to deal_dict
for store in store_list:

    # Go to store page 
    browser.get(store[1])
    time.sleep(1.0)

    # Select store
    clickButton(shop_at_this_store)
    time.sleep(3.0)
       
    # Go to BOGO page
    browser.get("https://www.publix.com/savings/weekly-ad/bogo")

    # Try clicking "Load More" button twice
    clickButton(loadmore)
    clickButton(loadmore)

    # Get page source
    html = browser.page_source
    soup = bs.BeautifulSoup(html)

    # Find all BOGO deals
    product_names = soup.findAll('span', {'class': 'p-text paragraph-md normal context--default color--null line-clamp title'})

    # Create empty list for each BOGO deal
    deal_list = []
    
    # Add BOGO products to list
    for i in range(len(product_names)):
        deal_list.append(product_names[i].text.strip())

    # Add store name and BOGO products to dict
    deal_dict[store[0]] = deal_list


# Close browser
browser.close()

# Convert dictionary to pandas dataframe to later on use pandas built in to_html function
deals_DF = pd.DataFrame.from_dict(data = deal_dict, orient = 'columns')

# Email BOGO deals
yag = yagmail.SMTP(GMAIL_username , GMAIL_password)
subject = 'Publix BOGO Deals'
body = deals_DF.to_html(justify = 'center' , col_space = 20) # Convert dataframe to HTML
yag.send(to = target_email, subject = subject, contents = body)
