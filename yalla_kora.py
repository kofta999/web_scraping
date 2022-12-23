import requests
from bs4 import BeautifulSoup
import csv
import datetime

date = input("Please enter a date in form MM/DD/YYYY ")
try:
    datetime.datetime.strptime(date, '%m/%d/%Y')
except ValueError:
    raise ValueError("Incorrect data format, should be MM/DD/YYYY")

page = requests.get(f"https://www.yallakora.com/Match-Center/?date={date}")
match_list = []

def main(page):
    soup = BeautifulSoup(page.content, "lxml")
    championships = soup.find_all("div", {"class": "matchCard"})

    def get_match_data(championship):
        championship_title = championship.contents[1].contents[1].contents[-2].text.strip()
        match_details = championship.contents[3].find_all('li')

        for match in match_details:
            match = match.contents[1].contents[1]
            match_type = match.find("div", {"class": "date"}).text.strip()
            match_status = match.find("div", {"class": "matchStatus"}).find("span", {"class": "status"}).text.strip()

            team_A = match.find("div", {"class": "teamA"}).text.strip()
            team_B = match.find("div", {"class": "teamB"}).text.strip()
            score = match.find("div", {"class": "MResult"}).find_all("span", {"class": "score"})
            score = f"{score[0].text.strip()} - {score[1].text.strip()}"
            time = match.find("div", {"class": "MResult"}).find("span", {"class": "time"}).text.strip()


            match_list.append({"نوع البطولة": championship_title, "نوع المباراة": match_type,
                "حالة المباراة": match_status, "الفريق الاول": team_A, "الفريق الثاني": team_B, "النتيجة": score, "الوقت": time})



    for i in range(len(championships)):
        get_match_data(championships[i])

    with open("yalla_kora.csv", "w") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=match_list[0].keys())
        writer.writeheader()
        writer.writerows(match_list)
        print("File Created")


main(page)
