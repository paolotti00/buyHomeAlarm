import logging
import service.scrape_soup_utility_service as scrape_soup_utility_service
from model.classes import Home, Site


# immobiliare
from model.search_home_classes import HomeUserSearch


def get_data_immobiliare(query_urls: [str], supported_site_conf: Site) -> [Home]:
    logging.info("start to elaborate '%s' site", supported_site_conf.site_name)
    # todo fix the empty case
    homes_to_return = [Home]
    for query_url in query_urls:
        if supported_site_conf.api_case_string in query_url:
            homes_to_return += get_from_api_immobiliare(query_url)
        else:
            homes_to_return += scrape_immobiliare(scrape_soup_utility_service.get_soup(query_url), supported_site_conf)
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
            home_item.id_from_site = site.site_name + "_" + item["id"]
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


def convert_to_site(home_user_search: HomeUserSearch) -> Site:
    # todo
    to_return: Site = Site()
    return to_return
