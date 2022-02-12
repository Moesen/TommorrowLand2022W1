import requests
from bs4 import BeautifulSoup
import json

url = "https://www.tomorrowland.com/en/festival/line-up/stages/friday-15-july-2022"

if __name__ == "__main__":
    artists = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    
    days = soup.find_all("div", class_="eventday")
    for day in days[:3]:
        stages = day.find_all("div", class_="stage")
        for stage in stages:
            content = stage.find_all("li")
            for con in content:
                name = con.text.replace("\n", "").lstrip().rstrip()
                artists.append(name)

    with open("artists.json", "w") as f:
        f.write(json.dumps(artists, indent=2))