import logging

from model.classes import Home, Site, Search
from constant.constants import IMMOBILIARE_SITE_NAME, IDEALISTA_SITE_NAME, CASA_IT_SITE_NAME
from service.config_service import get_supported_site_conf
from service.repository_service import Repository
from service.scrape_casa_it_service import get_data_casa_it
from service.scrape_idealista_service import get_data_idealista
from service.scrape_immobiliare_service import get_data_immobiliare


def scrape_data(job_id) -> [Search]:
    repository = Repository()
    logging.info("start to get data from searches")
    searches: [Search] = repository.get_searches_from_job_id(job_id)
    n_homes_found = 0
    for search in searches:
        homes_to_return = []
        logging.info("start to elaborate search %s", search.title)
        for site in search.sites:
            if site.query_urls and len(site.query_urls) > 0:
                logging.info("start to elaborate site %s, it have %s query_urls", site.site_name, len(site.query_urls))
                if site.site_name.casefold() == IMMOBILIARE_SITE_NAME.casefold():
                    homes_to_return += get_data_immobiliare(site.query_urls, get_supported_site_conf(site.site_name))
                elif site.site_name.casefold() == IDEALISTA_SITE_NAME.casefold():
                    homes_to_return += get_data_idealista(site.query_urls, get_supported_site_conf(site.site_name))
                elif site.site_name.casefold() == CASA_IT_SITE_NAME.casefold():
                    homes_to_return += get_data_casa_it(site.query_urls, get_supported_site_conf(site.site_name))
            else:
                logging.info("no query_urls in search %s site %s", search.title, site.site_name)
        search.homes = homes_to_return
        n_homes_found = n_homes_found + len(homes_to_return)
        logging.info("finished search %s", search.title)
    logging.info("get data from searches finished, found %s in %s searches", n_homes_found, len(searches))
    return searches


def get_only_the_new_homes(homes: [Home]):
    logging.info("evaluating how many new homes of these %s homes", len(homes))
    repository = Repository()
    homes_to_return = []
    for home in homes:
        if not home or home.id_from_site is None or len(repository.get_home_by_id_from_site(home.id_from_site)) > 0:
            continue
        homes_to_return.append(home)
    logging.info("there are %s new homes from %s homes", len(homes_to_return), len(homes))
    return homes_to_return


def order_home_by_price(homes: [Home]):
    homes.sort(key=Home.get_price)
    return homes


def check_if_already_sent_it():
    return True
