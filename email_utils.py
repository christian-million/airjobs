import smtplib
import keyring
from email.message import EmailMessage
from email.headerregistry import Address
from jinja2 import Template
from datetime import datetime


def render_template(path, **kwargs):
    '''Renders a Template (Shortcut for a common templating workflow)

    Arguments
    ---------
    path: str
        Path to the template
    **kwargs:
        Arguments to the template
    '''

    # Read the raw template
    with open(path, 'r') as f:
        string = f.read()

    # Convert raw template to template class
    template = Template(string)

    # Render the template
    x = template.render(kwargs)

    return x


def send_email(subject, text, html):
    '''Sends an email to my work email with contents of `html` (or `text` if recipient turns off html).

    Arguments
    ---------
    subject: str
        Subject line for email
    text: str
        A message to email in plain text
    html: str
        An html message to email
    '''

    # I've registered my local machine to know what these are
    # (Only works if I am logged in on my machine as me)
    username = keyring.get_password('airjobs', 'username')
    password = keyring.get_password('airjobs', 'password')

    if username is None or password is None:

        with open('log.txt', 'a') as f:
            f.write(f"{datetime.now()}\n")
            f.write("\tNo username/password in keyring for `airjobs`\n")

        raise ValueError("No username/password in keyring for `airjobs`\n")

    # Create the EmailMessage object and assign attributes
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = Address('Christian Million', username, 'gmail.com')
    msg['To'] = Address('Christian Million', 'millionc', 'yosemite.edu')

    # Add plain text message
    msg.set_content(text)

    # Alternative added second so it is prioritized when sending
    msg.add_alternative(html, subtype='html')

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(username, password)

    # If I can't email myself an error message, then I should log it.
    except smtplib.SMTPException as e:
        with open('log.txt', 'a') as f:
            f.write(f"{datetime.now()}\n")
            f.write(f"\tSMTP Error {e.smtp_code}: {e.smtp_error}\n")

    else:
        server.send_message(msg)

    finally:
        # This will fail is server = smtplib.SMTP("smtp.gmail.com", 587) fails,
        # but we will have already logged the error by this point.
        server.quit()
