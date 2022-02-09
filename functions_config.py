import yaml
import os
from yaml import UnsafeLoader
import constants as Constant
from classes import Config, Search, Site
import argparse
import logging


# this function permit to convert a dict to object recursively #https://joelmccune.com/python-dictionary-as-object/
class DictObj:
    def __init__(self, in_dict: dict):
        assert isinstance(in_dict, dict)
        for key, val in in_dict.items():
            if isinstance(val, (list, tuple)):
                setattr(self, key, [DictObj(x) if isinstance(x, dict) else x for x in val])
            else:
                setattr(self, key, DictObj(val) if isinstance(val, dict) else val)


def config_app():
    parser = argparse.ArgumentParser(description="buyhomealarm")
    # [Define arguments here]
    parser.add_argument('--environment', required=True,
                        help="must specify " + Constant.ENV_ENVIROMENT_DEV_VALUE + "  or " + Constant.ENV_ENVIROMENT_DEV_VALUE)
    args = parser.parse_args()
    os.environ[Constant.ENV_ENVIROMENT_ENV] = args.environment
    logging.info('from cmd line --enviroment = %s', args.environment)


def get_enviroment_env() -> str:
    return os.getenv(Constant.ENV_ENVIROMENT_ENV) or Constant.DEFAULT_ENV or Constant.DEFAULT_ENV


def get_config() -> Config:
    to_return: Config
    environment = get_enviroment_env()
    config_file_name = None
    if environment == Constant.ENV_ENVIROMENT_DEV_VALUE:
        config_file_name = Constant.CONFIG_FILE_DEV_NAME
    elif environment == Constant.ENV_ENVIROMENT_PROD_VALUE:
        config_file_name = Constant.CONFIG_FILE_PROD_NAME
    with open(config_file_name, "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=UnsafeLoader)
        # to_return = namedtuple('struct', cfg.keys())(*cfg.values())
        to_return = DictObj(cfg)
        logging.info('%s was loaded', config_file_name)
        return to_return


def get_email_config():
    return get_config().email


def get_db_config():
    return get_config().db


def get_searches() -> [Search]:
    return get_config().searches


def get_supported_site_conf(site_name) -> [Site]:
    for supported_sites_conf in get_config().supported_sites_conf:
        if supported_sites_conf.site_name.casefold() == site_name:
            return supported_sites_conf
