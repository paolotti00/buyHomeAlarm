import os
import time


def start_sched_and_keep_alive(scheduler):
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()


def clean_price_and_convert_to_int(price: str) -> int:
    # example € 298.000€ 330.000(-8,0%)
    # 298000 330000(-9,7%)
    # 298000
    return int(price.replace("€", "").replace(".", "").strip().split(" ")[0].strip())


def convert2serialize(obj):
    if isinstance(obj, dict):
        return {k: convert2serialize(v) for k, v in obj.items()}
    elif hasattr(obj, "_ast"):
        return convert2serialize(obj._ast())
    elif not isinstance(obj, str) and hasattr(obj, "__iter__"):
        return [convert2serialize(v) for v in obj]
    elif hasattr(obj, "__dict__"):
        return {
            k: convert2serialize(v)
            for k, v in obj.__dict__.items()
            if not callable(v) and not k.startswith('_')
        }
    else:
        return obj


def return_empty_if_not_exist_attribute(test):
    try:
        return test
    except AttributeError:
        return ""
