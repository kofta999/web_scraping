import time

from selenium import webdriver

# define the global variables
USERNAME = ''
EMAIL = ''
PASSWORD = ''

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

# navigate to the LinkedIn user followed companies page
driver.get(f'https://www.linkedin.com/in/{USERNAME}/details/interests/?detailScreenTabIndex=1')

# wait for 5 seconds
time.sleep(5)
for i in range(20):
    driver.execute_script('window.scrollBy(0, 500);')

# locate the elements that contain the names of the companies the user follows
companies = []
for i in range(100):
    try:
        companies.append(driver.find_element(by='css selector', value=f'#profilePagedListComponent-ACoAADoHiB4BHKlhuTXkEDWpyLt0JhaKOhNCo0g-INTERESTS-VIEW-DETAILS-profileTabSection-COMPANIES-INTERESTS-NONE-en-US-{i} > div > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > a > div > span > span:nth-child(1)').text)
    except:
        continue
# create an empty list to store the company names
print(companies)
