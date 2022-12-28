import time
import csv
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup

USERNAME = ''
EMAIL = ''
PASSWORD = ''
links_fr = []
data = []


options = Options()
# options.add_argument("--headless")
options.add_argument("user-data-dir=C:\\Users\\SOUQ COMPUTER\\AppData\\Local\\Microsoft\\Edge\\User Data")
driver = webdriver.Edge(options=options)

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
