import logging

from model.classes import Home, Site
import service.scrape_soup_utility_service as scrape_soup_utility_service


# casa it
def get_data_casa_it(query_urls: [str], supported_site_conf) -> [Home]:
    logging.info("start to elaborate '%s' site", supported_site_conf.site_name)
    homes_to_return = []
    for query_url in query_urls:
        homes_to_return += scrape_casa_it(scrape_soup_utility_service.get_soup(query_url), supported_site_conf)
    logging.info("end to elaborate %s site, found %s homes", supported_site_conf.site_name, len(homes_to_return))
    return homes_to_return


def scrape_casa_it(soup, site: Site):
    # todo check if no blocked
    homes_to_return = []
    items = soup.findAll("article")
    for item in items:
        home_item: Home = Home()
        home_item.origin_site = site.site_name

        # decode
        try:
            home_item.id_from_site = site.site_name + "_" + item.find("div", {"class": "srp-card__anc"})["id"]
        except (AttributeError, TypeError, KeyError) as e:
            pass
        try:
            home_item.link_detail = site.base_url + item.find("a")["href"]
        except (AttributeError, TypeError, KeyError) as e:
            pass
        try:
            home_item.title = item.find("div", {"class": "art-addr"}).find("a")["title"]
        except (AttributeError, TypeError, KeyError) as e:
            pass
        try:
            home_item.price = item.find("div", {"class": "info-features__price"}, recursive=False).find("p").text
        except (AttributeError, TypeError, KeyError) as e:
            pass
        try:
            home_item.parking = item.find("div", {"class": "is-box"}).text
        except (AttributeError, TypeError, KeyError) as e:
            pass
        try:
            home_item.description = item.find("div", {"class": "art-desc__content"}).text
        except (AttributeError, TypeError, KeyError) as e:
            pass
        try:
            for item_detail in item.findAll("div", {"class": "info-features__item"}):
                # check if mt2
                if "mq" in item_detail.text:
                    home_item.mt2 = item_detail.text
                elif "locali" in item_detail.text:
                    home_item.n_rooms = item_detail.text
        except (AttributeError, TypeError, KeyError) as e:
            pass
        # todo date
        # add element
        homes_to_return.append(home_item)
    return homes_to_return
