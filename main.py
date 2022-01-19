import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

SITE_NAME_IMMOBILIARE = "IMMOBILIARE"
SITE_NAME_IDEALISTA = "IDEALISTA"


class Home:
    def __init__(self, zone, price, title):
        self.zone = zone
        self.price = price
        self.title = title


def get_soup(url):
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    # }
    # # create an HTML Session object
    # session = HTMLSession()
    #
    # # Use the object above to connect to needed webpage
    # resp = session.get(url, headers=headers)
    #
    # # Run JavaScript code on webpage
    # resp.html.render()
    # return BeautifulSoup(resp.html.html, "html.parser")
    headers = requests.utils.default_headers()
    headers.update({"user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0"})
    brainly = requests.get(url, headers=headers)
    return BeautifulSoup(brainly.text, "html5lib")


def scrape_immobiliare(soup):
    home_result = Home
    return home_result


def scrape_idealista(soup):
    home_result = Home
    return home_result


def scrape_data(soup, site_name):
    home = None
    if site_name == SITE_NAME_IMMOBILIARE:
        home = scrape_immobiliare(soup)
    elif site_name == SITE_NAME_IDEALISTA:
        home = scrape_immobiliare(scrape_idealista)
    print(soup)


scrape_data(get_soup("https://www.idealista.it/"), SITE_NAME_IMMOBILIARE)
