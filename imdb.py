import requests
from bs4 import BeautifulSoup
import csv

year = input("Enter a year to search top movies for\n")

try:
    if int(year) < 1874 or int(year) > 2029:
        raise ValueError("Invalid Date")
except:
    raise TypeError("Enter a year in format YYYY")

url = f"http://www.imdb.com/search/title?release_date={year}"
page = requests.get(url)
soup = BeautifulSoup(page.content, "lxml")
movie_data = []

movie_names = soup.find_all("h3", {"class": "lister-item-header"})
certificate_length_genres = soup.find_all("div", {"class": "lister-item-content"})
ratings = soup.find_all("div", {"class": "inline-block ratings-imdb-rating"})


for i in range(len(movie_names)):
    movie_name = movie_names[i].text.replace("\n", " ").strip()
    certificate = certificate_length_genres[i].find("span", {"class": "certificate"})
    try:
        length = certificate_length_genres[i].find("span", {"class": "runtime"}).text
    except:
        length = "TBA"
    try:
        genres = certificate_length_genres[i].find("span", {"class": "genre"}).text.strip()
    except:
        genres = "TBA"
    try:
        rating = ratings[i].strong.text.strip()
    except:
        rating = "TBA"
    description = certificate_length_genres[i].find_all("p", {"class": "text-muted"})[1].text.strip()

    if certificate is None:
        certificate = "TV-14"
    else:
        certificate = certificate.text


    movie_data.append({
        "Movie Name": movie_name, "Certificate": certificate,
        "Length": length, "Genres": genres,
        "Rating": rating, "Description": description
        })

with open("imdb.csv", 'w') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=movie_data[0].keys())
    writer.writeheader()
    writer.writerows(movie_data)
    print("File Created")
