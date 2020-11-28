# Webscraping

# Goals

- Every morning, scrape the [AIR Job Board](https://www.airweb.org/resources/job-board) and email me any new positions


# Sources

- https://docs.python.org/3/library/email.examples.html
- https://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python/27515833#27515833
- https://docs.python.org/3/library/smtplib.html
- https://jinja.palletsprojects.com/en/2.11.x/


# Psuedo Code

- Scrape the jobs into a list-like format

- Compare the running list with today's scrape and identify new ones

- Add new ones to running list

- Compile each new job into a list and prep for email

- Email links to newly posted jobs (if any)

