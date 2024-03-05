import csv
import requests
from bs4 import BeautifulSoup

url = "https://nmamit.nitte.edu.in/"
HEADERS = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36', 'Accept-Language': 'en-US,en q=0.5'}
website = requests.get(url, headers=HEADERS)

soup = BeautifulSoup(website.text, 'lxml')
courses = []
link_to_course = []
target_div = soup.find("div", id="Undergraduate")

if target_div:
    ul_tag = target_div.find('ul')

    if ul_tag:
        li_tags = ul_tag.find_all('li')

        for li in li_tags:
            cou = li.text
            courses.append(cou)
            a_tag = li.find('a')
            if a_tag:
                text = a_tag.get_text(strip=True)
                hr = a_tag['href']
                href = "https://nmamit.nitte.edu.in/" + hr
                link_to_course.append(href)


def scrape_data_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    faculties = soup.find_all('div', class_='col-xs-12 col-sm-12 col-md-3')
    faculty_names = []
    for faculty in faculties:
        name = faculty.find("div", class_="content").find('h3')
        if name:
            faculty_names.append(name.text.strip())
    return faculty_names


# Create a dictionary to store course names and their corresponding faculties
courses_faculties = {}

for idx, url in enumerate(link_to_course):
    course_name = courses[idx]
    faculties = scrape_data_from_url(url)
    courses_faculties[course_name] = faculties

# Write data to CSV file
with open('nmamit_course_faculties.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Course_Name', 'Faculties', 'Course_link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for course_name, faculties in courses_faculties.items():
        writer.writerow({'Course_Name': course_name, 'Faculties': ', '.join(faculties), 'Course_link': link_to_course[courses.index(course_name)]})
