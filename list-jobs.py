import pandas as pd
import requests

from bs4 import BeautifulSoup



jobs_list = list()

def extract(page):
    url =f"https://www.seek.com.au/junior-project-manager-jobs/in-All-Sydney-NSW?page={page}"
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'lxml')
    return soup

def transform(soup):
    article = soup.find_all("article")
    for art in article:
        title = art.find("a", class_="_2S5REPk").text
        company  = art.find("a", class_="_17sHMz8").text
        try:
            salary = art.find("span", class_="_7ZnNccT").text
            description  = art.find("ul", class_="_3uiq0PN").get_text(separator="; ")
        except:
            salary=""
            description =""

        jobs_link = ("https://www.seek.com.au/")+ art.find("a", class_="_2S5REPk")['href']

        job = dict(title=title,company=company, salary=salary, description=description, jobs_link=jobs_link.rsplit("?")[0])
        jobs_list.append(job)

print("Comenzando scraping ........\n")

for i in range(1,6):
    print(f"Scraping de la página: {i}")
    extract_lis = extract(i)
    transform(extract_lis)

df = pd.DataFrame(jobs_list)
pd.set_option("display.max_rows", None)
print(df.head())

df.to_csv('list_jobs.csv', index=False)