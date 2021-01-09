import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np
import random

def extract(location: str, pages: int):
    location = location.lower()
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
    j = 1    
    all_jobs = list()
    for i in range(0, pages + 1, 10):
        print("page {} getting scraped".format(j))
        url = "https://in.indeed.com/jobs?q&l={}&start={}".format(
            location, i)
        random_header = random.choice(headers)    
        r = requests.get(url, random_header)
        soup = BeautifulSoup(r.content, 'html.parser')

        elements = soup.find_all('div', class_="jobsearch-SerpJobCard")

        jobs = dict()

        for elem in elements:
            try:
                title = elem.find('a', class_="jobtitle turnstileLink").text.strip()
                salary = elem.find('span', class_="salaryText").text.strip()
                company = elem.find('span', class_="company").text.strip()
                description = elem.find('li').text.strip()
                posted = elem.find('span', class_="date").text.strip()
                jobs = {
                    "title": title,
                    "salary": salary,
                    "company": company,
                    "description": description,
                    "posted": posted
                }
            except Exception as e:
                jobs = {
                    "title": "None",
                    "salary": "None",
                    "company": "None",
                    "description": "None",
                    "posted": "None"
                }
            all_jobs.append(jobs)
        j += 1    

    return all_jobs    

start = time.time()
print("Scraping started")

jobs_list = list()
jobs_list = extract("hyderabad",100)

print("Total Time taken:",time.time() - start)

data = pd.DataFrame()
data['title'] = np.nan
data['salary'] = np.nan
data['company'] = np.nan
data['description'] = np.nan
data['posted'] = np.nan

index = 0

for i in range(len(jobs_list)):
    data.loc[index, 'title'] = jobs_list[i]['title']
    data.loc[index, 'salary'] = jobs_list[i]['salary']
    data.loc[index, 'company'] = jobs_list[i]['company']
    data.loc[index, 'description'] = jobs_list[i]['description']
    data.loc[index, 'posted'] = jobs_list[i]['posted']
    index += 1

print(data.shape)