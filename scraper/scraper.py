import requests
from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')

browser = webdriver.Chrome(options = chrome_options)

URL = "https://www.frontiersin.org/articles?journal=276"

browser.get(URL)
time.sleep(1)

body = browser.find_element(By.TAG_NAME, 'body')
for _ in range(10):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)

page = browser.page_source
browser.quit()

soup = BeautifulSoup(page, "html.parser")

# results = soup.find(id = 'CardWrapper')

articles = soup.find_all('article', class_ = "CardArticle")

print(len(articles))
for article in articles:
    # navigate to link in href
    link = article.find('a')['href']
    # print(link)
    #open link
    article_page = requests.get(link)
    article_soup = BeautifulSoup(article_page.content, "html.parser")
    # find article title
    title = article_soup.find('div', class_ = "JournalAbstract__titleWrapper")
    authors = []
    for author in article_soup.find('div', class_ = "authors").find_all('span', class_ = "author-wrapper"):
        author_name = author.find('a')
        if author_name:
            name = author_name.text.strip()
        else:
            name = ''.join(author.stripped_strings)
        cleaned_name = re.sub(r'[\d†*]+$', '', name).strip()
        authors.append(cleaned_name)
    print(title.text.strip())
    print(authors)
