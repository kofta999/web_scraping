import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
# define the global variables
USERNAME = 'mahmoud-abdelghany-rageh'
EMAIL = ''
PASSWORD = ''

# create a new Chrome browser
options = Options()
options.add_argument("user-data-dir=C:\\Users\\Mahmoud Abdelghany\\AppData\\Local\\Google\\Chrome\\User Data")
driver = webdriver.Chrome(options=options)

#login for the first time only

# navigate to the LinkedIn login page
#driver.get('https://www.linkedin.com/login')

# # locate the email and password input elements
# email_input = driver.find_element(by='id', value='username')
# password_input = driver.find_element(by='id', value='password')
#
# # locate the login button
# login_button = driver.find_element(by='xpath', value='//button[@type="submit"]')
#
# # enter your email and password
# email_input.send_keys(EMAIL)
# password_input.send_keys(PASSWORD)
#
# # click the login button
# login_button.click()

# wait for 5 seconds
#time.sleep(5)

company = 'https://www.linkedin.com/company/209215/'
# navigate to the LinkedIn company posts
driver.get(f'{company}/posts/?feedView=all')
time.sleep(5)
#scroll some posts
for i in range(11):
    driver.execute_script('window.scrollBy(0, 500);')
soup = BeautifulSoup(driver.page_source, 'lxml')

posts = soup.find_all("div", {"class": "feed-shared-update-v2__description-wrapper"})
for i in range(len(posts)):
    posts[i] = str(posts[i].find("span", {"class": "break-words"}))
#print(posts[0])
for post in posts:
    if( post.find('internship') != -1 or post.find('intern') != -1 or post.find('منحة') != -1 or post.find('تدريب') != -1):
        #company is a place holder
        print(f"found intern at #company# post number {posts.index(post)}")
