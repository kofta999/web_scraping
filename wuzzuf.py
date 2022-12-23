import requests
# from requests_html import HTMLSession
from bs4 import BeautifulSoup
import csv

#title = input("Enter your job title ")
# session = HTMLSession()
page_num = 0
jobs = [] # List of dicts to put each job's full details at

while True:
    page = requests.get(f"https://wuzzuf.net/search/jobs/?q=devops&start={page_num}")
    soup = BeautifulSoup(page.content, "lxml")
    jobs_amount = soup.find("span", {"class": "css-xkh9ud"}).strong.text.strip()

    if page_num >= (int(jobs_amount) // 15):
        break

    dates = []
    salaries = []
    good_job_titles = []
    good_company_names = []
    good_locations = []
    good_job_skills = []
    good_dates = []
    good_job_type = []
    good_job_links = []

    job_titles = soup.find_all("h2", {"class": "css-m604qf"})
    company_names = soup.find_all("a", {"class": "css-17s97q8"})
    locations = soup.find_all("span", {"class": "css-5wys0k"})
    job_skills = soup.find_all("div", {"class": "css-y4udm8"})
    recent_dates = soup.find_all("div", {"class": "css-4c4ojb"})
    old_dates = soup.find_all("div", {"class": "css-do6t5g"})
    job_type = soup.find_all("span", {"class": "css-1ve4b75 eoyjyou0"})
    dates = [*recent_dates, *old_dates]

    for i in range(len(job_titles)):
        good_job_titles.append(job_titles[i].text.strip())
        good_company_names.append(company_names[i].text.strip()[:-2])
        good_locations.append(locations[i].text.strip())
        good_job_skills.append(job_skills[0].find_all("div")[1].text.strip())
        good_dates.append(dates[i].text.strip())
        good_job_type.append(job_type[i].text.strip())
        jobs.append({"Job Title": good_job_titles[i], "Company Name": good_company_names[i],
        "Job Type": good_job_type[i], "Location": good_locations[i], "Job Skills": good_job_skills[i], "Date Posted": good_dates[i]})



    page_num += 1
    print("Page Switched")





with open("wuzzuf.csv", 'w') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=jobs[0].keys())
    writer.writeheader()
    writer.writerows(jobs)
    print("File Created")
