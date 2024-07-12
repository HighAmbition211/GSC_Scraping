from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
from bs4 import BeautifulSoup
import ssl
import smtplib
import requests

sent_emails = []


sender = 'm'
password = ''
appPassword = ''

searchKeyword = ["site:gfe.foundation"]
body = "site:gfe.foundation"

message = 'Subject: {}\n\n {}'.format(
    'Get More Customers By HighAmbition211',
    body)

context = ssl.create_default_context()
port = 465
host = "smtp.gmail.com"

mail_server = smtplib.SMTP_SSL(host=host, port=port, context=context)

# Path of the chrome driver
PATH = "C:\Program Files (x86)\chromedriver-win64\chromedriver.exe"
driver = webdriver.Chrome(PATH)

try:
    mail_server.login(sender, appPassword)
except smtplib.SMTPAuthenticationError as e:
    print("Failed to login, error: ", e)
    exit(1)

link_extensions = ['', 'contact', 'contact-us', 'contact.html', 'contact-us.html']

def createSearchTerm(searchkeyword):
    originalSearchTerm = "https://www.google.com/search?q="
    for element in searchkeyword:
        originalSearchTerm += element.replace(" ", "+") + "+"
    print("originalSearchTerm : ", originalSearchTerm)
    return originalSearchTerm

def check_email(emails):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    regex2 = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$' #"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9-.]+"
    for email in emails:
        # Check if the text is an email address
        if(re.search(regex,email) or re.search(regex2, email)):  
            print("Valid Email")
            print("\t" + email)
            if email not in sent_emails:
                sendemail(email)
                sent_emails.append(email)
            print(sent_emails)
            return True
            break
        else:
            print("Invalid Email")
            if len(email) <= 195:
                print("\t" + email)
            else:
                pass

def sendemail(email):
    receiver = email
    # Send an email
    mail_server.sendmail(sender, receiver, message)
    print("Email successfully sent to {}!".format(receiver))
    time.sleep(2)

def validurl(link):
    # Check the validity of the URL. In this case, we only want to scrape the homepages of websites.
    pattern = "(https://|http://)+(|www.)+[a-zA-Z0-9.-]+.(com|net|co|org|us|info|biz|me)+(|/)"
    p = re.compile(pattern)
    if(re.fullmatch(p, link)):
            for extension in link_extensions:
                try:
                    source = requests.get(link + extension, timeout=10)
                    soup = BeautifulSoup(source.text, 'lxml')
                    print("Looking for emails in " + link + extension)
                    # Look for emails on the website
                    find_emails = soup.body.findAll(text=re.compile('@')) #instead of re.findall
                    check_email(find_emails)
                    if check_email(find_emails):
                        break
                except Exception as e:
                    print(f"Error fetching URL: {e}")
    # else:
    #         print("False")

driver.get(createSearchTerm(searchKeyword))
driver.implicitly_wait(5)
parentElement = driver.find_elements_by_class_name("yuRUbf")
for element in parentElement:
    elementList = element.find_element_by_tag_name("a")
    link = elementList.get_attribute("href")
    validurl(link)
    print(link)
print("Finished scraping for URLs!")
driver.quit()