import logging
from pynput import keyboard
from tap_tap import TapTap

logging.basicConfig(
    filename='tap_tap.log', 
    level=logging.DEBUG, 
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def on_release(key):
    global tap_tap
    try:
        logging.debug(f'{key} pressed')
        return tap_tap.on_release_impl(key)
    except Exception as e:
        logging.error(f"Error: {e}")
    return True

tap_tap = TapTap()

def main():
    # Collect events until released
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    logging.info('start listending on ctrl_l')
    try:
        main()
        logging.info('end listending on ctrl_l')
    except Exception as e:
        logging.error(f"Error: {e}")
