import smtplib
import keyring
from email.message import EmailMessage
from email.headerregistry import Address
from json import load


def send_email(text, html):

    username = keyring.get_password("airjobs", "username")
    password = keyring.get_password("airjobs", "password")

    # Create message container - the correct MIME type is multipart/alternative.
    msg = EmailMessage()
    msg['Subject'] = "New AIR Job Posting"
    msg['From'] = Address('Christian Million', username, 'gmail.com')
    msg['To'] = Address('Christian Million', 'millionc', 'yosemite.edu')

    msg.set_content(text)
    msg.add_alternative(html, subtype='html')

    # Send the message via local SMTP server.
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.send_message(msg)
    server.quit()


def prep_html(jobs=None):

    pretty_jobs ="<ul>"
    for job in jobs:
        pretty_jobs += f'''\
            <li><a href='{job[1]}'>{job[0]}</a> in {job[3]}</li>
                <ul>
                    <li>Institution: {job[2]}</li>
                    <li>Salary: {job[4]}</li>
                    <li>Due: <b>{job[5]}</b></li>
                </ul>
            '''
    pretty_jobs += "</ul>"
        

    out = f'''\
    <html>
        <head>
        <title>New AIR Job Posting</title>
        </head>
    <body>

    <h1>New Opportunities</h1>
    <p>Good morning, Christian! Looks like a new job or two have been posted to the <a href="https://www.airweb.org/resources/job-board">AIR Job Board</a>.</p>

    {pretty_jobs}

    <p>Best,<br>Yourself</p>
    </body>
    </html>
    '''
    return out

def prep_text(jobs):

    pretty_jobs = ""
    for job in jobs:
        pretty_jobs += f'''\
            - {job[0]} in {job[3]}
            \t- Link: {job[1]}
            \t- Institution: {job[2]}
            \t- Salary: {job[4]}
            \t- {job[5]}
            '''

    out = f'''\
    Good morning, Christian!
    
    Looks like a new job or two have been posted to the AIR Job Board (https://www.airweb.org/resources/job-board).

    {pretty_jobs}

    Best,
    Yourself
    '''
    return out
