import requests
from bs4 import BeautifulSoup
import pandas as pd

lap_name = []
lap_price = []
lap_rating = []
buy_link =[]

for i in range(1, 20):  # Corrected loop to start from page 1
    url = "https://www.flipkart.com/laptops/~laptops-under-rs60000/pr?sid=6bo%2Cb5g&page=" + str(i)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    box = soup.find("div", class_="_1YokD2 _3Mn1Gg")
    
    if box is not None:  # Check if box is not None
        name = box.find_all("div", class_="_4rR01T")
        price = box.find_all("div", class_="_30jeq3 _1_WHN1")
        rating = box.find_all("div", class_="_3LWZlK")
        links = box.find_all("a", class_="_1fQZEK")

        for i, _ in enumerate(price):
            pr = _.text
            lap_price.append(pr)

            if i < len(rating):
                pr = rating[i].text
            else:
                pr = None  # Set to None if rating not available
            lap_rating.append(pr)

        for i in name:
            pr = i.text
            lap_name.append(pr)
        for i in links:
            pr = i.get('href')
            comp = "https://www.flipkart.com" + pr
            buy_link.append(comp)
    else:
        print(f"No laptops found on page {i}")

df = pd.DataFrame({"Rating": lap_rating, "Name": lap_name, "Price": lap_price, "Buy Link": buy_link})
df.to_csv("Under60000.csv", index=False)  # index=False to avoid writing row indices to CSV


