import logging

from model.classes import Home, Site

# idealista
import service.scrape_soup_utility_service as scrape_soup_utility_service
from model.search_home_classes import HomeUserSearch


def get_data_idealista(query_urls: [str], supported_site_conf) -> [Home]:
    logging.info("start to elaborate '%s' site", supported_site_conf.site_name)
    homes_to_return = []
    for query_url in query_urls:
        homes_to_return += scrape_idealista(scrape_soup_utility_service.get_soup(query_url), supported_site_conf)
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
            home_item.id_from_site = site.site_name + "_" + item["data-adid"]
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


def convert_to_site(home_user_search: HomeUserSearch) -> Site:
    # todo
    to_return: Site = Site()
    return to_return
