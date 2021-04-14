from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import time

import email
import smtplib
import ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from variables import VARIABLES

# Actual URL
# url_to_scrape = "https://covid19vaccine.health.ny.gov/"

# URL I used for testing 
url_to_scrape = "http://127.0.0.1:5500/index.html"

count = 0
running = True

def email(count):
    V = VARIABLES()
    subject = "ELIGIBILITY UPDATED " + str(count)
    body = "IT'S GO TIME!"
    # To be filled in with your own credentials 
    sender_email = V.sender_email
    receiver_email = V.receiver_email
    password = V.password

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

while running: 
    time.sleep(1)

    # Get the html from the website
    req = Request(url_to_scrape, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    html_soup = BeautifulSoup(webpage, 'html.parser')

    # Go through our html, and pull all the divs with a specific class
    eligibility_items = html_soup.find_all('span', class_="eligibility__content")

    matches = ['age', 'Age']

    for item in eligibility_items:
        if any(x in item.text for x in matches):
            count = count + 1
            if '30' in item.text:
                print('Request', count, '-> Still age 30')
            else:
                print('Request', count, '-> Eligibility updated!')
                running = False

for x in range(1, 20):
    email(count)
    print('Email sent to Kev', x)
    count = count + 1
    time.sleep(10)