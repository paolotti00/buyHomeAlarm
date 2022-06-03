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
    # todo mortgage fix ValueError: invalid literal for int() with base 10: '298000 330000(-9,7%)'
    return int(price.replace("€", "").replace(".", "").strip())
