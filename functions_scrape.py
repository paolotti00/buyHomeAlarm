from datetime import datetime

import requests
from bs4 import BeautifulSoup

from classes import Home, Message
from constants import IMMOBILIARE_SITE_NAME, IDEALISTA_SITE_NAME, IDEALISTA_BASE_URL, IMMOBILIARE_URL, IDEALISTA_URL, \
    DATE_PATTERN


def get_soup(url):
    headers = requests.utils.default_headers()
    headers.update({"user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0"})
    return BeautifulSoup(requests.get(url, headers=headers).text, "html5lib")


def scrape_data() -> [Home]:
    homes = []
    homes += scrape_data_(IMMOBILIARE_SITE_NAME)
    homes += scrape_data_(IDEALISTA_SITE_NAME)
    return homes


def scrape_data_(site_name) -> [Home]:
    homes_to_return = []
    if site_name == IMMOBILIARE_SITE_NAME:
        homes_to_return += scrape_immobiliare(get_soup(IMMOBILIARE_URL))
    elif site_name == IDEALISTA_SITE_NAME:
        homes_to_return += scrape_idealista(get_soup(IDEALISTA_URL))
    return homes_to_return


def scrape_immobiliare(soup):
    homes_to_return = []
    items = soup.findAll("li", {"class": "in-realEstateResults__item"})
    for item in items:
        home_item: Home = Home()
        home_item.origin_site = IMMOBILIARE_SITE_NAME
        try:
            # decode
            home_item.id = IMMOBILIARE_SITE_NAME + "_" + item["id"]
            home_item.link_detail = item.find("div", {"class": "nd-mediaObject__content"}).a["href"]
            home_item.title = item.find("div", {"class": "nd-mediaObject__content"}).a["title"]
            home_item.price = item.find("li", {"class": "in-realEstateListCard__features--main"}).text
            home_item.description = item.find("p", {"class": "in-realEstateListCard__descriptionShort"}).text
            home_item.description_short = item.find("div", {"class": "in-realEstateListCard__caption"}).text
            home_item.mt2 = item.find("li", {"aria-label": "superficie"}).text
            home_item.floor = item.find("li", {"aria-label": "piano"}).text
            home_item.n_rooms = item.find("li", {"aria-label": "locali"}).text
            # home_item.date = item.find("li", {"aria-label": "data vendita"}).text #fixme
            home_item.n_bath_rooms = item.find("li", {"aria-label": "bagni"}).text
            # add element
            homes_to_return.append(home_item)
        except (AttributeError, TypeError, KeyError) as e:
            # fixme: find how to not skip the entire object in case of error, maybe i can use suppress()
            # do nothing and go ahead
            # print(e)
            pass
    return homes_to_return


def scrape_idealista(soup):
    homes_to_return = []
    items = soup.findAll("article")
    for item in items:
        home_item: Home = Home()
        home_item.origin_site = IDEALISTA_SITE_NAME
        try:
            # decode
            home_item.id = IDEALISTA_SITE_NAME + "_" + item["data-adid"]
            home_item.link_detail = IDEALISTA_BASE_URL + item.find("a", {"class": "item-link"})["href"]
            home_item.title = item.find("p", {"class": "item-highlight-phrase"})["title"]
            home_item.price = item.find("span", {"class": "item-price"}).text
            home_item.parking = item.find("span", {"class": "item-parking"}).text
            home_item.description = item.find("div", {"class": "description"}).text
            for item_detail in item.findAll("span", {"class": "item-detail"}):
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


def get_only_the_new(homes: [Home]):
    homes_to_return = []
    for home in homes:
        # todo check on db
        homes_to_return.append(home)
    return homes_to_return


def create_message(homes: [Home]):
    message = Message()
    message.is_sent = False
    message.creation_date = datetime.today().strftime(DATE_PATTERN)
    message.homes = homes
    return message


def check_if_already_sent_it():
    return True



