import requests
from bs4 import BeautifulSoup

SITE_NAME_IMMOBILIARE = "IMMOBILIARE"
SITE_NAME_IDEALISTA = "IDEALISTA"
URL_IDEALISTA = "https://www.idealista.it/aree/vendita-case/?shape=%28%28%7Dom%7EFsgpjAyqGa%7B%40enJdPihBquEmkB%7DlPjnEghNdnIgqEpqPhoFdrBtqGeB%60iGkuAxwQ_rG%7EcC%29%29"
URL_IMMOBILIARE = "https://www.idealista.it/aree/vendita-case/?shape=%28%28%7Dom%7EFsgpjAyqGa%7B%40enJdPihBquEmkB%7DlPjnEghNdnIgqEpqPhoFdrBtqGeB%60iGkuAxwQ_rG%7EcC%29%29"

class Home:
    def __init__(self, zone, price, title):
        self.zone = zone
        self.price = price
        self.title = title


def get_soup(url):
    headers = requests.utils.default_headers()
    headers.update({"user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0"})
    return BeautifulSoup(requests.get(url, headers=headers).text, "html5lib")


def scrape_immobiliare(soup):
    home_result = Home
    return home_result


def scrape_idealista(soup):
    print(soup)
    home_result = Home
    return home_result


def scrape_data(site_name):
    home = None
    if site_name == SITE_NAME_IMMOBILIARE:
        home = scrape_immobiliare(get_soup(URL_IDEALISTA))
    elif site_name == SITE_NAME_IDEALISTA:
        home = scrape_idealista(get_soup(URL_IMMOBILIARE))


scrape_data(SITE_NAME_IDEALISTA)
