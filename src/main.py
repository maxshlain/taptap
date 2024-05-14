# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import logging
from pynput import keyboard
from tap_tap import TapTap

tap_tap = TapTap()

logging.basicConfig(
    filename='tap_tap.log',
    level=logging.DEBUG,
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def on_release(key): # Assign a value to the tap_tap variable
    try:
        logging.debug('%s pressed', key)
        return tap_tap.on_release_impl(key)
    except Exception as on_release_exception: # pylint: disable=broad-except
        logging.error("Error: %s", on_release_exception)
    return True

def main():
    # Collect events until released
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    logging.info('start listending on ctrl_l')
    try:
        main()
        logging.info('end listending on ctrl_l')
    except Exception as e: # pylint: disable=broad-except
        logging.error("Error: %s", e)
