import requests
from bs4 import BeautifulSoup
import sqlite3


def get_content(url):
    page =requests.get(url)
    # print(page)
    soup = BeautifulSoup(page.content, "html.parser")
    # print(soup)
    quotes = soup.find_all("div", class_="quote")
    # print(quotes)
    quote_list = []
    for quote in quotes:
        text = quote.find("span", class_="text").text
        author = quote.find("small", class_="author").text
        # print(text)
        quote_list.append({"text":text,"author":author})
    add_to_database(quote_list)

def add_to_database(quote_list):

    conn = sqlite3.connect(("quotes.db"))


    conn.execute('''
    CREATE  TABLE IF NOT EXISTS quotes_data(
    quotes text,
    authors text
    );''')

    print("Table created successfully")

    # Inserting Values
    for quote in quote_list:
        conn.execute("INSERT INTO quotes_data (quotes, authors) VALUES (?, ?)", (quote['text'], quote['author']))



    conn.commit()
    conn.close()


if __name__ == "__main__":
    url = "https://quotes.toscrape.com/"
    get_content(url)
