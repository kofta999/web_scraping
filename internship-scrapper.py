import time

from selenium import webdriver
from bs4 import BeautifulSoup

# define the global variables
USERNAME = ''
EMAIL = ''
PASSWORD = ''
links_fr = []

# create a new Chrome browser
driver = webdriver.Chrome()

# navigate to the LinkedIn login page
driver.get('https://www.linkedin.com/login')

# locate the email and password input elements
email_input = driver.find_element(by='id', value='username')
password_input = driver.find_element(by='id', value='password')

# locate the login button
login_button = driver.find_element(by='xpath', value='//button[@type="submit"]')

# enter your email and password
email_input.send_keys(EMAIL)
password_input.send_keys(PASSWORD)

# click the login button
login_button.click()

# wait for 5 seconds
time.sleep(5)
print("here1")
# navigate to the LinkedIn user followed companies page
driver.get(f'https://www.linkedin.com/in/{USERNAME}/details/interests/?detailScreenTabIndex=1')

time.sleep(2)
print("here2")

soup = BeautifulSoup(driver.page_source, 'lxml')

links = soup.find_all("a", {"data-field": "active_tab_companies_interests", "target": "_self"})

for i in range(len(links)):
    links_fr.append(links[i].attrs["href"])
    
links_fr = set(links_fr)

print(links_fr)
driver.quit()


