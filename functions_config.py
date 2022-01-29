import yaml
from yaml import UnsafeLoader

from classes import Config, Search, Site


# this function permit to convert a dict to object recursively #https://joelmccune.com/python-dictionary-as-object/
class DictObj:
    def __init__(self, in_dict: dict):
        assert isinstance(in_dict, dict)
        for key, val in in_dict.items():
            if isinstance(val, (list, tuple)):
                setattr(self, key, [DictObj(x) if isinstance(x, dict) else x for x in val])
            else:
                setattr(self, key, DictObj(val) if isinstance(val, dict) else val)


def get_config() -> Config:
    to_return: Config
    with open("config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=UnsafeLoader)
        # to_return = namedtuple('struct', cfg.keys())(*cfg.values())
        to_return = DictObj(cfg)
        return to_return


def get_email_config():
    return get_config().email


def get_searches() -> [Search]:
    return get_config().searches


def get_supported_site_conf(site_name) -> [Site]:
    for supported_sites_conf in get_config().supported_sites_conf:
        if supported_sites_conf.site_name.casefold() == site_name:
            return supported_sites_conf
