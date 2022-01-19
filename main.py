import requests
from bs4 import BeautifulSoup

SITE_NAME_IMMOBILIARE = "IMMOBILIARE"
SITE_NAME_IDEALISTA = "IDEALISTA"
URL_IDEALISTA = "https://www.idealista.it/aree/vendita-case/?shape=%28%28%7Dom%7EFsgpjAyqGa%7B%40enJdPihBquEmkB%7DlPjnEghNdnIgqEpqPhoFdrBtqGeB%60iGkuAxwQ_rG%7EcC%29%29"
URL_IMMOBILIARE = "https://www.idealista.it/aree/vendita-case/?shape=%28%28%7Dom%7EFsgpjAyqGa%7B%40enJdPihBquEmkB%7DlPjnEghNdnIgqEpqPhoFdrBtqGeB%60iGkuAxwQ_rG%7EcC%29%29"


class Home:
    title = None
    price = None
    zone = None
    mt2 = None
    link_detail = None
    origin_site = None


def get_soup(url):
    headers = requests.utils.default_headers()
    headers.update({"user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0"})
    return BeautifulSoup(requests.get(url, headers=headers).text, "html5lib")


def scrape_immobiliare(soup):
    home_result = Home
    return home_result


def scrape_idealista(soup):
    homes_to_return = []
    articles = soup.findAll("article")
    for article in articles:
        home_item: Home = Home()
        home_item.origin_site = SITE_NAME_IDEALISTA
        try:
            # decode
            # home_item.title = article.find("p", {"class": "item-highlight-phrase"})
            # home_item.price = article.find("span", {"class": "item-price"}).text
            home_item.title = article.find("p", {"class": "item-highlight-phrase"})["title"]
            home_item.price = article.find("span", {"class": "item-price"}).text
            # add element
            homes_to_return.append(home_item)
        except Exception:
            # do nothing
            continue
    return homes_to_return


def scrape_data(site_name) -> [Home]:
    homes = [Home]
    if site_name == SITE_NAME_IMMOBILIARE:
        homes += scrape_immobiliare(get_soup(URL_IMMOBILIARE))
    elif site_name == SITE_NAME_IDEALISTA:
        homes += scrape_idealista(get_soup(URL_IDEALISTA))
    return homes


for home in scrape_data(SITE_NAME_IDEALISTA):
    print(home.title)
    print(home.price)
    print("---")
