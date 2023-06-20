"""
This script uses the Selenium and BeautifulSoup libraries to scrape LinkedIn for internship opportunities.

It requires the following arguments to be defined:
- USERNAME: the LinkedIn username of the user whose profile page will be accessed
- EMAIL: the LinkedIn email of the user (required for logging in)
- PASSWORD: the LinkedIn password of the user (required for logging in)

To use this script, you will need to install the following libraries:
- selenium
- beautifulsoup4

You will also need to have the Chrome browser installed, and specify the path to the ChromeDriver executable in the
code.

To use a pre-existing login session for LinkedIn, specify the "user-data-dir" argument in the ChromeOptions object.
This will allow the script to access the user's LinkedIn profile page and search for posts without requiring the user
to manually log in.

To run the script, you will need to:
1. Define the USERNAME, EMAIL, and PASSWORD variables.
2. Uncomment the block of code that logs in to LinkedIn (if you want to log in for the first time).
3. Run the script.

The script will scrape LinkedIn for internship opportunities by:
1. Navigating to the LinkedIn profile page of the user specified in the USERNAME variable.
2. Generating a list of company names and their LinkedIn profile links that the user has listed as interests.
3. Searching for posts on the LinkedIn profiles of the companies that contain the word "internship".
4. Storing the company name, post text, and post link in a csv file.
"""
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
USERNAME = '' # Insert your LinkedIn user-name here.
EMAIL = ''  # Insert your LinkedIn email here.
PASSWORD = ''  # Insert your LinkedIn password here.
links_fr = []
data = []
options = Options()
options.add_argument("--headless")   # comment this line if you want the browser to be visible
options.add_argument("user-data-dir=C:\\Users\\USER NAME\\AppData\\Local\\Google\\Chrome\\User Data")
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
# # Enter your email and password.
# email_input.send_keys(EMAIL)
# password_input.send_keys(PASSWORD)
#
# # Click the login button.
# login_button.click()

def company_names_generator():
    driver.get(f'https://www.linkedin.com/in/{USERNAME}/details/interests/?detailScreenTabIndex=1')

    time.sleep(5)
    for i in range(20):
        driver.execute_script('window.scrollBy(0, 500);')

    companies_names = []
    for i in range(100):
        try:
            companies_names.append(driver.find_element(by='css selector', value=f'#profilePagedListComponent-ACoAADoHiB4BHKlhuTXkEDWpyLt0JhaKOhNCo0g-INTERESTS-VIEW-DETAILS-profileTabSection-COMPANIES-INTERESTS-NONE-en-US-{i} > div > div > div.display-flex.flex-column.full-width.align-self-center > div.display-flex.flex-row.justify-space-between > a > div > span > span:nth-child(1)').text)
        except:
            continue

    links_fr =[]
    soup = BeautifulSoup(driver.page_source, 'lxml')

    links = soup.find_all("a", {"data-field": "active_tab_companies_interests", "target": "_self"})

    for i in range(len(links)):
        if "?legacySchoolId=" not in links[i].attrs["href"]:
            links_fr.append(links[i].attrs["href"])
            links_fr = list(dict.fromkeys(links_fr))

    companies = {}
    for company in companies_names:
        for link in links_fr:
            companies[company] = link
            links_fr.remove(link)
            break

    return companies

def post_searcher(companies):
    for company, link in companies.items():
        driver.get(f'{link}/posts/?feedView=all')
        time.sleep(5)

        for i in range(11):
            driver.execute_script('window.scrollBy(0, 500);')

        soup = BeautifulSoup(driver.page_source, 'lxml')
        posts = soup.find_all("div", {"class": "feed-shared-update-v2__description-wrapper"})

        for i in range(len(posts)):
            posts[i] = posts[i].find("span", {"class": "break-words"})
            if "internship" in str(posts[i]) or "منحة" in str(posts[i]) or "تدريب" in str(posts[i]):
                data.append({"Notification": f"Found intern opportunity at {company} in post number {i+1}",
                    "Post Details": posts[i].text})

if __name__ == "__main__":
    companies = company_names_generator()
    post_searcher(companies)

    with open("results.csv", 'w', encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=["Notification", "Post Details"])
        writer.writeheader()
        writer.writerows(data)
        print("File Created")

    driver.quit()
