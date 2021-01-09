import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np
import random


def getHeaders():
    headers = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
               "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
               "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",
               "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
               "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"
               ]

    return headers           

def getPages(location: str):
    url = "https://internshala.com/internships/internship-in-{}".format(location)
    random_header = random.choice(getHeaders())
    r = requests.get(url, random_header)
    soup = BeautifulSoup(r.content, 'html.parser')

    pages = int(soup.find('span', id="total_pages").text.strip())

    return pages


def extract(location: str):
    location = location.lower()   
    all_jobs = list()
    total_pages = getPages(location)
    print("Scraping total of {} pages".format(total_pages))
    for i in range(1, total_pages + 1):
        print("Scraping page {}".format(i))
        url = "https://internshala.com/internships/internship-in-{}/page-{}".format(
            location, i)
        random_header = random.choice(getHeaders())
        print(random_header)  
        r = requests.get(url, random_header)
        soup = BeautifulSoup(r.content, 'html.parser')

        elements = soup.find_all(
            'div', class_="individual_internship")

        jobs = dict()

        for elem in elements:
            try:
                title = elem.find('div', class_="company").text.strip().split('  ')[0]
            except Exception:
                title = np.nan

            try:
                location = elem.find('a', class_="location_link").text.strip()
            except Exception:
                location = np.nan

            try:
                company = elem.find(
                    'a', class_="link_display_like_text").text.strip()
            except Exception:
                company = np.nan

            try:
                start = elem.find(
                    'span', class_="start_immediately_desktop").text.strip()
            except Exception:
                start = np.nan

            try:
                duration = elem.find_all('div', class_="item_body")[1].text.strip()
            except Exception:
                duration = np.nan

            try:
                stipend = elem.find('span', class_="stipend").text.strip()
            except Exception:
                stipend = np.nan

            try:
                apply_by = elem.find_all('div', class_="item_body")[3].text.strip()
            except Exception:
                apply_by = np.nan

            try:
                tags = elem.find('div', class_="tags_container").text.strip()
            except Exception:
                tags = np.nan

            try:
                link = elem.find('div', class_="profile")['href'].text.strip()
            except Exception:
                link = np.nan
  
            jobs = {
                "title": title,
                "location": location,
                "company": company,
                "start":start,
                "duration":duration,
                "stipend": stipend,
                "apply by":apply_by,
                "tags":tags,
                "link":link
            }
            
            all_jobs.append(jobs)   
    return all_jobs    


location = input("Enter the location where you want the job:")
start = time.time()
print("Scraping started")

jobs_list = list()
jobs_list = extract(location)

print("Total Time taken:", time.time() - start)

data = pd.DataFrame()
data['title'] = np.nan
data['location'] = np.nan
data['company'] = np.nan
data['start'] = np.nan
data['duration'] = np.nan
data['stipend'] = np.nan
data['apply_by'] = np.nan
data['tags'] = np.nan
data['link'] = np.nan

index = 0

for i in range(len(jobs_list)):
    data.loc[index, 'title'] = jobs_list[i]['title']
    data.loc[index, 'location'] = jobs_list[i]['location']
    data.loc[index, 'company'] = jobs_list[i]['company']
    data.loc[index, 'start'] = jobs_list[i]['start']
    data.loc[index, 'duration'] = jobs_list[i]['duration']
    data.loc[index, 'stipend'] = jobs_list[i]['stipend']
    data.loc[index, 'apply_by'] = jobs_list[i]['apply by']
    data.loc[index, 'tags'] = jobs_list[i]['tags']
    data.loc[index, 'link'] = jobs_list[i]['link']
    index += 1

print(data.shape)
print(data.isnull().sum())
print("*"*50)
print(data.head())