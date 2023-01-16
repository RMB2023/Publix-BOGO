from selenium import webdriver
import time
import bs4 as bs

# Variables:
loadmore = '//*[@id="main"]/div[4]/div/div[2]/div[2]/div[4]/button/span'
web_driver_path = r'C:\Users\YOUR PATH HERE'

browser = webdriver.Chrome(executable_path = web_driver_path)

browser.get("https://www.publix.com/savings/weekly-ad/bogo")

def clickButton(path):
    try:
        browser.find_element_by_xpath(path).click()
        pass
    except Exception:
        time.sleep(1.0)
        clickButton(path)

time.sleep(3.0)

# Try clicking "load more" button twice
clickButton(loadmore)
clickButton(loadmore)

time.sleep(1.0)

# Get page source
html = browser.page_source

# Close browser
browser.close()

# soup = bs.BeautifulSoup(html, features='html5lib')
soup = bs.BeautifulSoup(html)

# Find all BOGO deals
product_names = soup.findAll('span', {'class': 'p-text paragraph-md normal context--default color--null line-clamp title'})

# Create empty dictionary to store deals
deal_dict = {}

# Add BOGO products to dictionary
for i in range(len(product_names)):
    deal_dict[i] = product_names[i].text.strip()

# Print deals
print(deal_dict)
