import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://nmamit.nitte.edu.in/professional-clubs.php"
HEADERS = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36', 'Accept-Language': 'en-US,en q=0.5'}
website = requests.get(url, headers=HEADERS)

soup = BeautifulSoup(website.text, 'lxml')
table = soup.find("table", class_="rwd-table table table-bordered table-striped")
headers = table.find_all('th')
header = []
for i in headers:
    h = i.text
    header.append(h)

df = pd.DataFrame(columns=header)
rows = table.find_all('tr')
for i in rows[1:]:
    data = i.find_all('td')
    row = [tr.text for tr in data]
    
    # Pad the row with empty strings if its length is less than the number of columns
    if len(row) < len(header):
        row += [''] * (len(header) - len(row))
    
    l = len(df)
    df.loc[l] = row

df.to_csv("IEEEStudentBranchEventWinners.csv")
print("done")
