# todo check if can delete this
def common_init(self, d=None):
    if d is not None:
        for key, value in d.items():
            # print("key --> " + key + " " + "value --> " + str(value))
            if isinstance(value, list) and isinstance(value[0], dict):
                for item in value:
                    common_init(getattr(type(self), key)[0], dict(item))
            if isinstance(value, list):
                if isinstance(value[0], dict):
                    continue
            setattr(self, key, value)
