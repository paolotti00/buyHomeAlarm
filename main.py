import requests
from bs4 import BeautifulSoup

IMMOBILIARE_SITE_NAME = "IMMOBILIARE"
IMMOBILIARE_URL = "https://www.idealista.it/aree/vendita-case/?shape=%28%28%7Dom%7EFsgpjAyqGa%7B%40enJdPihBquEmkB%7DlPjnEghNdnIgqEpqPhoFdrBtqGeB%60iGkuAxwQ_rG%7EcC%29%29"
IDEALISTA_SITE_NAME = "IDEALISTA"
IDEALISTA_URL = "https://www.idealista.it/aree/vendita-case/?shape=%28%28%7Dom%7EFsgpjAyqGa%7B%40enJdPihBquEmkB%7DlPjnEghNdnIgqEpqPhoFdrBtqGeB%60iGkuAxwQ_rG%7EcC%29%29"
IDEALISTA_BASE_URL = "https://www.idealista.it/"


class Home:
    id = None
    title = None
    price = None
    zone = None
    mt2 = None
    floor = None
    n_rooms = None
    parking = None
    description = None
    link_detail = None
    origin_site = None
    date = None


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
        home_item.origin_site = IDEALISTA_SITE_NAME
        try:
            # decode
            home_item.id = IDEALISTA_SITE_NAME + "_" + article["data-adid"]
            home_item.link_detail = IDEALISTA_BASE_URL + article.find("a", {"class": "item-link"}).text
            home_item.title = article.find("p", {"class": "item-highlight-phrase"})["title"]
            home_item.price = article.find("span", {"class": "item-price"}).text
            home_item.parking = article.find("span", {"class": "item-parking"}).text
            home_item.description = article.find("div", {"class": "description"}).text
            for item_detail in article.findAll("span", {"class": "item-detail"}):
                # check if mt2
                if "m2" in item_detail.text:
                    home_item.mt2 = item_detail.text
                elif "piano" in item_detail.text:
                    home_item.floor = item_detail.text
                elif "local" in item_detail.text:
                    home_item.n_rooms = item_detail.text
            # todo date
            # add element
            homes_to_return.append(home_item)
        except (AttributeError, TypeError, KeyError) as e:
            # fixme: find how to not skip the entire object in case of error, maybe i can use suppress()
            # do nothing and go ahead
            # print(e)
            pass
    return homes_to_return


def scrape_data(site_name) -> [Home]:
    homes = [Home]
    if site_name == IMMOBILIARE_SITE_NAME:
        homes += scrape_immobiliare(get_soup(IMMOBILIARE_URL))
    elif site_name == IDEALISTA_SITE_NAME:
        homes += scrape_idealista(get_soup(IDEALISTA_URL))
    return homes


for home in scrape_data(IDEALISTA_SITE_NAME):
    print(vars(home))
    print("---")
