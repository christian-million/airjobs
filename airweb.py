import requests
from bs4 import BeautifulSoup
import csv as csv
import email_utils as em

def get_posted_jobs():
    URL = "https://www.airweb.org/resources/job-board"

    response = requests.get(URL)
    response_text = BeautifulSoup(response.text, "html.parser")

    scraped_jobs = response_text.find_all('tr', class_='job-item')

    job_data = [['title', 'link', 'institution', 'location', 'salary', 'due']]

    for job in scraped_jobs:
        title = job.find('td', class_='title').text.strip()
        link = job.find('td', class_='title').find('a', href=True)['href']
        institution = job.find('td', class_='institution').text.strip()
        location = job.find('td', class_='location').text.strip()
        salary = job.find('td', class_='salary').text.strip()
        due = job.find('td', class_='app-due-date').text.strip()
        job_data.append([title, link, institution, location, salary, due])
    
    return job_data


def get_running_jobs():
    with open('running_list.csv', newline='') as f:
        dat = list(csv.reader(f))

    return dat


def append_to_jobs(new_jobs):
    with open('running_list.csv', 'a', newline='') as f:
        w = csv.writer(f)
        w.writerows(new_jobs)


if __name__ == '__main__':

    posted_jobs = get_posted_jobs()
    running_jobs = get_running_jobs()

    new_jobs = []

    for row in posted_jobs:
        if row[1] not in [link[1] for link in running_jobs]:
            new_jobs.append(row)

    # Append to running list
    if new_jobs:
        append_to_jobs(new_jobs)
        em.send_email(em.prep_text(new_jobs), em.prep_html(new_jobs))