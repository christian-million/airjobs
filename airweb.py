import requests
from bs4 import BeautifulSoup
import csv as csv
from email_utils import render_template, send_email


def scrape_jobs():
    '''Scrapes the AIR Job Board and returns a list of jobs
    '''
    URL = "https://www.airweb.org/resources/job-board"

    response = requests.get(URL)
    response_text = BeautifulSoup(response.text, "html.parser")

    scraped_jobs = response_text.find_all('tr', class_='job-item')

    # Create the "headers"
    job_data = [['title', 'link', 'institution', 'location', 'salary', 'due']]

    # Get relevant information from each job
    for job in scraped_jobs:

        # Each attribute is in a table data element
        title = job.find('td', class_='title').text.strip()
        link = job.find('td', class_='title').find('a', href=True)['href']
        institution = job.find('td', class_='institution').text.strip()
        location = job.find('td', class_='location').text.strip()
        salary = job.find('td', class_='salary').text.strip()
        due = job.find('td', class_='app-due-date').text.strip()

        # Add information to running job list
        job_data.append([title, link, institution, location, salary, due])

    return job_data


def get_running_jobs():
    '''Gets jobs previously scraped and saved
    These will be used to compare against the fresh scrape.
    '''
    with open('running_list.csv', newline='') as f:
        dat = list(csv.reader(f))

    return dat


def append_to_jobs(new_jobs):
    '''Appends nes jobs to the running list of scraped jobs
    '''
    with open('running_list.csv', 'a', newline='') as f:
        w = csv.writer(f)
        w.writerows(new_jobs)


if __name__ == '__main__':

    # Scrape all jobs on website
    posted_jobs = scrape_jobs()

    if len(posted_jobs) <= 1:
        send_email("Check on the AIR Job script",
                   "Looks like something is wrong",
                   "<html><body><p>Looks like something is wrong</p></body></html>")

    # Load list of jobs that have already been scraped
    running_jobs = get_running_jobs()

    # Initialize a list to capture the new jobs
    new_jobs = []

    # Get a list of existing links
    existing_links = [link[1] for link in running_jobs]

    for row in posted_jobs:
        # This uses the link in each job description as the "unique" identifier
        # If a link does not show up in the running list of links, it is new, so add it to new_jobs
        if row[1] not in existing_links:
            new_jobs.append(row)

    # Append new jobs to running jobs and email about jobs
    if new_jobs:
        append_to_jobs(new_jobs)

        msg_txt = render_template("templates/new_job.txt", jobs=new_jobs)
        msg_html = render_template("templates/new_job.html", jobs=new_jobs)

        send_email("New AIR Job Posting", msg_txt, msg_html)
