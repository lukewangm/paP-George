import requests
from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import argparse
import sqlite3
import tqdm

def scrape(journal_name, URL):

    conn = sqlite3.connect('articles.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title TEXT,
            full_link TEXT,
            abstract TEXT
        )
    ''')
    
    conn.commit()

    # results = soup.find(id = 'CardWrapper')
    if journal_name == "Frontiers":
        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')

        browser = webdriver.Chrome(options = chrome_options)

        browser.get(URL)
        time.sleep(1)

        body = browser.find_element(By.TAG_NAME, 'body')
        for _ in range(10):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)

        page = browser.page_source
        browser.quit()

        soup = BeautifulSoup(page, "html.parser")
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
    elif journal_name == "Medical Case Reports":
        page = requests.get(URL + "/articles")
        # page = requests.get("https://jmedicalcasereports.biomedcentral.com/articles?searchType=journalSearch&sort=PubDate&page=149")
        soup = BeautifulSoup(page.content, "html.parser")
        iteration = 0

        while True:
            articles = soup.find_all('article', class_ = "c-listing__content")
            # print(URL)
            # print(len(articles))
            for article in tqdm.tqdm(articles, desc = "Scraping Articles"):
                title = article.find('h3', class_ = "c-listing__title").text.strip()
                metadata_div = article.find('div', class_="c-listing__metadata")

                if metadata_div:
                    # Find the span element with the data-test="result-list" attribute
                    content_type_span = metadata_div.find('span', {'data-test': 'result-list'})
                    
                    if content_type_span:
                        # Extract the text content, excluding the nested span
                        content_type = content_type_span.get_text(strip=True, separator=' ').replace('Content type: ', '')
                    # print(content_type)
                    if "Case report" not in content_type:
                        continue
                full_link = article.find('ul', class_="c-listing__view-options").find('a', {'data-test': 'fulltext-link'}).get('href')
                # print(URL + full_link)
                article_page = requests.get(URL + full_link)
                article_soup = BeautifulSoup(article_page.content, "html.parser")
                abstract_section = article_soup.find('section', {'aria-labelledby': 'Abs1'})
                if abstract_section:
                    abstract = abstract_section.get_text(separator='\n', strip=True)
                else:
                    continue
                cursor.execute('''
                    INSERT INTO articles (title, full_link, abstract)
                    VALUES (?, ?, ?)
                ''', (title, URL + full_link, abstract))
                conn.commit()
                # print(f"Title: {title}")
                # print(f"Link: {full_link}")
                # print(f"Abstract: {abstract}")
                # break


            # next page
            pagination = soup.find('ul', class_="c-pagination")
            next_page_link = pagination.find('a', rel="next")
            if next_page_link:
                next_page_url = next_page_link['href']
            else:
                break
            page = requests.get(URL + next_page_url)
            soup = BeautifulSoup(page.content, "html.parser")
            # if iteration == 1:
            #     break
            # iteration += 1
            
    conn.close()

def reset_db():
    conn = sqlite3.connect('articles.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
        DROP TABLE IF EXISTS articles
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title TEXT,
            full_link TEXT,
            abstract TEXT
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Scrape articles from Different Journals")
    parser.add_argument('--journal', type = str, help = "Journal Name")
    parser.add_argument('--reset', action = 'store_true', help = "Reset the database")
    args = parser.parse_args()
    url = ""
    if args.journal == "Frontiers":
        url = "https://www.frontiersin.org/articles?journal=276"
    elif args.journal == "Medical Case Reports":
        url = "https://jmedicalcasereports.biomedcentral.com"
    else:
        print("Please enter a valid journal name")
        exit()
    if args.reset:
        reset_db()
    scrape(args.journal, url)