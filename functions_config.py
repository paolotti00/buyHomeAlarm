from collections import namedtuple

import yaml
from yaml import UnsafeLoader

from classes import Site, Conf


# this function permit to convert a dict to object recursively #https://joelmccune.com/python-dictionary-as-object/
class DictObj:
    def __init__(self, in_dict: dict):
        assert isinstance(in_dict, dict)
        for key, val in in_dict.items():
            if isinstance(val, (list, tuple)):
                setattr(self, key, [DictObj(x) if isinstance(x, dict) else x for x in val])
            else:
                setattr(self, key, DictObj(val) if isinstance(val, dict) else val)


def get_config() -> Conf:
    to_return: Conf
    with open("config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=UnsafeLoader)
        # to_return = namedtuple('struct', cfg.keys())(*cfg.values())
        to_return = DictObj(cfg)
        return to_return


def get_email_config():
    return get_config().email


def get_sites() -> [Site]:
    return get_config().sites
