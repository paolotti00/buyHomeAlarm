import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from classes import Home, Message, Site, Search
from constants import IMMOBILIARE_SITE_NAME, IDEALISTA_SITE_NAME
from functions_config import get_config, get_searches, get_supported_site_conf
from functions_repository import Repository


def get_soup(url):
    headers = requests.utils.default_headers()
    headers.update({"user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0"})
    return BeautifulSoup(requests.get(url, headers=headers).text, "html5lib")


def scrape_data() -> [Home]:
    logging.info("start to get data from searches")
    searches: [Search] = get_searches()
    for search in searches:
        homes_to_return = []
        logging.info("start to elaborate search %s", search.title)
        for site in search.sites:
            if site.query_urls and len(site.query_urls) > 0:
                logging.info("start to elaborate site %s, it have %s query_urls", site.site_name, len(site.query_urls))
                if site.site_name.casefold() == IMMOBILIARE_SITE_NAME.casefold():
                    homes_to_return += get_data_immobiliare(site.query_urls, get_supported_site_conf(site.site_name))
                elif site.site_name.casefold() == IDEALISTA_SITE_NAME.casefold():
                    homes_to_return += get_data_idealista(site.query_urls,get_supported_site_conf(site.site_name))
            else:
                logging.info("no query_urls in search %s site %s",search.title, site.site_name)
        search.homes = homes_to_return
        logging.info("finished search %s", search.title)
    logging.info("get data from searches finished, found %s in %s searches", len(homes_to_return), len(searches))
    return searches


# immobiliare
def get_data_immobiliare(query_urls: [str], supported_site_conf: Site) -> [Home]:
    logging.info("start to elaborate '%s' site", supported_site_conf.site_name)
    # todo fix the empty case
    homes_to_return = [Home]
    for query_url in query_urls:
        if supported_site_conf.api_case_string in query_url:
            homes_to_return += get_from_api_immobiliare(query_url)
        else:
            homes_to_return += scrape_immobiliare(get_soup(query_url), supported_site_conf)
    logging.info("end to elaborate %s site, found %s homes", supported_site_conf.site_name, len(homes_to_return))
    return homes_to_return


def get_from_api_immobiliare(query_url) -> [Home]:
    # todo
    homes_to_return = []
    return homes_to_return


def scrape_immobiliare(soup, site: Site) -> [Home]:
    homes_to_return = []
    items = soup.findAll("li", {"class": "in-realEstateResults__item"})
    for item in items:
        home_item: Home = Home()
        home_item.origin_site = site.site_name
        # decode
        try:
            home_item.id = site.site_name + "_" + item["id"]
        except (AttributeError, TypeError, KeyError) as e:
            # do nothing and go ahead
            # print(e)
            pass
        try:
            home_item.link_detail = item.find("div", {"class": "nd-mediaObject__content"}).a["href"]
        except (AttributeError, TypeError, KeyError) as e:
            # do nothing and go ahead
            # print(e)
            pass
        try:
            home_item.title = item.find("div", {"class": "nd-mediaObject__content"}).a["title"]
        except (AttributeError, TypeError, KeyError) as e:
            # do nothing and go ahead
            # print(e)
            pass

        try:
            home_item.price = item.find("li", {"class": "in-realEstateListCard__features--main"}).text
        except (AttributeError, TypeError, KeyError) as e:
            pass
        try:
            home_item.description = item.find("p", {"class": "in-realEstateListCard__descriptionShort"}).text
        except (AttributeError, TypeError, KeyError) as e:
            pass
        try:
            home_item.description_short = item.find("div", {"class": "in-realEstateListCard__caption"}).text
        except (AttributeError, TypeError, KeyError) as e:
            pass
        try:
            home_item.mt2 = item.find("li", {"aria-label": "superficie"}).text
        except (AttributeError, TypeError, KeyError) as e:
            pass
        try:
            home_item.floor = item.find("li", {"aria-label": "piano"}).text
        except (AttributeError, TypeError, KeyError) as e:
            pass
        try:
            home_item.n_rooms = item.find("li", {"aria-label": "locali"}).text
        except (AttributeError, TypeError, KeyError) as e:
            pass
        # home_item.date = item.find("li", {"aria-label": "data vendita"}).text #fixme
        try:
            home_item.n_bath_rooms = item.find("li", {"aria-label": "bagni"}).text
        except (AttributeError, TypeError, KeyError) as e:
            pass
        # add element
        homes_to_return.append(home_item)
    return homes_to_return


# idealista
def get_data_idealista(query_urls: [str], supported_site_conf) -> [Home]:
    logging.info("start to elaborate '%s' site", supported_site_conf.site_name)
    homes_to_return = []
    for query_url in query_urls:
        homes_to_return += scrape_idealista(get_soup(query_url), supported_site_conf)
    logging.info("end to elaborate %s site, found %s homes", supported_site_conf.site_name, len(homes_to_return))
    return homes_to_return


def scrape_idealista(soup, site: Site):
    homes_to_return = []
    items = soup.findAll("article")
    for item in items:
        home_item: Home = Home()
        home_item.origin_site = site.site_name

        # decode
        try:
            home_item.id = site.site_name + "_" + item["data-adid"]
        except (AttributeError, TypeError, KeyError) as e:
            pass
        try:
            home_item.link_detail = site.base_url + item.find("a", {"class": "item-link"})["href"]
        except (AttributeError, TypeError, KeyError) as e:
            pass
        try:
            home_item.title = item.find("a", {"class": "item-link"})["title"]
        except (AttributeError, TypeError, KeyError) as e:
            pass
        try:
            home_item.price = item.find("span", {"class": "item-price"}).text
        except (AttributeError, TypeError, KeyError) as e:
            pass
        try:
            home_item.parking = item.find("span", {"class": "item-parking"}).text
        except (AttributeError, TypeError, KeyError) as e:
            pass
        try:
            home_item.description = item.find("div", {"class": "description"}).text
        except (AttributeError, TypeError, KeyError) as e:
            pass
        try:
            for item_detail in item.findAll("span", {"class": "item-detail"}):
                # check if mt2
                if "m2" in item_detail.text:
                    home_item.mt2 = item_detail.text
                elif "piano" in item_detail.text:
                    home_item.floor = item_detail.text
                elif "local" in item_detail.text:
                    home_item.n_rooms = item_detail.text
        except (AttributeError, TypeError, KeyError) as e:
            pass
        # todo date
        # add element
        homes_to_return.append(home_item)
    return homes_to_return


def get_only_the_new_homes(homes: [Home]):
    logging.info("evaluating how many new homes of these %s homes", len(homes))
    repository = Repository()
    homes_to_return = []
    for home in homes:
        if not home or home.id is None or len(repository.get_home(home.id)) > 0:
            continue
        homes_to_return.append(home)
    logging.info("there are %s new homes from %s homes", len(homes_to_return), len(homes))
    return homes_to_return


def create_message(searches: [Search]):
    message = Message()
    message.is_sent = False
    # message.creation_date = datetime.today().strftime(get_config().conf.date_pattern) #todo fix invalid format name
    # message.zones = zones #fixme bson error
    return message


def check_if_already_sent_it():
    return True
