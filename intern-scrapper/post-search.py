import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup

# Define the global variables for the LinkedIn email, password, and username.
USERNAME = 'mahmoud-abdelghany-rageh'
EMAIL = ''  # Insert your LinkedIn email here.
PASSWORD = ''  # Insert your LinkedIn password here.

# Create a new Chrome browser with the "user-data-dir" argument specified.
# This allows the script to use a pre-existing login session for LinkedIn.
options = Options()
options.add_argument("user-data-dir=C:\\Users\\Mahmoud Abdelghany\\AppData\\Local\\Google\\Chrome\\User Data")
driver = webdriver.Chrome(options=options)

# Uncomment the following block of code if you want to login for the first time.
# # Navigate to the LinkedIn login page.
# driver.get('https://www.linkedin.com/login')
#
# # Locate the email and password input elements.
# email_input = driver.find_element(by='id', value='username')
# password_input = driver.find_element(by='id', value='password')
#
# # Locate the login button.
# login_button = driver.find_element(by='xpath', value='//button[@type="submit"]')
#
# email_input.send_keys(EMAIL)
# password_input.send_keys(PASSWORD)
#
# # Click the login button.
# login_button.click()

# Define the URL of the LinkedIn company page.
company = 'https://www.linkedin.com/company/209215/'

# Navigate to the LinkedIn company page and wait for 5 seconds.
driver.get(f'{company}/posts/?feedView=all')
time.sleep(5)

# Scroll through the company's posts.
for i in range(11):
    driver.execute_script('window.scrollBy(0, 500);')

# Use the BeautifulSoup library to parse the HTML of the page and locate the elements containing the company's posts.
soup = BeautifulSoup(driver.page_source, 'lxml')
posts = soup.find_all("div", {"class": "feed-shared-update-v2__description-wrapper"})

# Iterate through the posts, searching for the keywords of interest. If any are found, print a message indicating the post number.
for i in range(len(posts)):
    posts[i] = str(posts[i].find("span", {"class": "break-words"}))
    if "internship" in posts[i] or "intern" in posts[i] or "منحة" in posts[i] or "تدريب" in posts[i]:
        print(f"Found intern opportunity at #company# in post number {i}")
