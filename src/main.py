import time
import logging
from pynput import keyboard

# Setup logging
logging.basicConfig(
    filename='keystrokes.log', 
    level=logging.INFO, 
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

last_caps_lock_press_time = 0
double_press_interval = 999  # milliseconds
max_keystrokes = 999
keystrokes = []
last_word_keystrokes = []
keyboard_controller = keyboard.Controller()

def delete_before_type_in_next_layout(count):
    i = 0
    while i < count:
        i += 1
        keyboard_controller.press(keyboard.Key.backspace)
        keyboard_controller.release(keyboard.Key.backspace)
        time.sleep(0.2)

def type_in_next_layout(word):
    for key in word:
        keyboard_controller.press(key)
        keyboard_controller.release(key)
        time.sleep(0.2)

def switch_layout():
    keyboard_controller.press(keyboard.Key.ctrl)
    keyboard_controller.press(keyboard.Key.shift)
    keyboard_controller.press(keyboard.Key.alt)
    keyboard_controller.press(keyboard.Key.space)
    keyboard_controller.release(keyboard.Key.space)
    keyboard_controller.release(keyboard.Key.alt)
    keyboard_controller.release(keyboard.Key.shift)
    keyboard_controller.release(keyboard.Key.ctrl)

def is_signal_key(key):
    return key == keyboard.Key.ctrl_l

def milliseconds_since_last_signal(last_caps_lock_press_time):
    interval = (time.time() - last_caps_lock_press_time) * 1000
    return int(interval)

def on_signal(key):
    global last_caps_lock_press_time

    logging.info(f"Signal received: {key}")

    if last_caps_lock_press_time == 0:
        last_caps_lock_press_time = time.time()
        return

    current_interval = milliseconds_since_last_signal(last_caps_lock_press_time)
    if current_interval > double_press_interval:
        logging.info(f"too big interval: {current_interval}")
        last_caps_lock_press_time = time.time()
        return

    if last_caps_lock_press_time != 0 and current_interval < double_press_interval:
        last_caps_lock_press_time = time.time()
        last_word = get_last_word()
        logging.info(f"last_word: {last_word}")
        switch_layout()
        delete_before_type_in_next_layout(len(last_word))
        type_in_next_layout(last_word)

    return True

def get_char(key):
    try:
        return key.char
    except AttributeError:
        return None

def count_pressed_chars_since_last_whitespace():
    i = len(keystrokes) - 1
    last_whitespace_index = -1
    while i >= 0:
        next_key = keystrokes[i]
        i -= 1

        next_char = get_char(next_key)
        if not next_char:
            last_whitespace_index = -1
            continue

        if next_key == keyboard.Key.space or next_key == keyboard.Key.enter:
            if last_whitespace_index == -1:
                last_whitespace_index = i
            else:
                return len(keystrokes) - i - 1
    # end while
    return len(keystrokes)

def get_last_word():

    if len(keystrokes) < 1:
        logging.info("No keystrokes to log")
        return

    last_word_text = ''
    i = len(keystrokes) - 1
    first_whitespace_index = -1
    non_space_seen = False
    while i >= 0:
        next_key = keystrokes[i]
        i -= 1

        next_char = get_char(next_key)
        if next_char:
            non_space_seen = True

        if next_key == keyboard.Key.space or next_key == keyboard.Key.enter:
            if non_space_seen and first_whitespace_index == -1:
                first_whitespace_index = i + 1
    # end while

    result_keystrokes = []
    if first_whitespace_index == -1:
        for keystroke in keystrokes:
            next_char = get_char(keystroke)
            if next_char:
                last_word_text += get_char(keystroke)
                result_keystrokes.append(keystroke)
        logging.info(f"last_word_text: {last_word_text}")
        return result_keystrokes
    
    i = first_whitespace_index
    while i < len(keystrokes):
        next_key = keystrokes[i]
        i += 1
        next_char = get_char(next_key)
        if next_char:
            last_word_text += get_char(next_key)
            result_keystrokes.append(next_key)
    logging.info(f"last_word_text: {last_word_text}")
    return result_keystrokes
    
def record_keystroke(key):
    keystrokes.append(key)
    if len(keystrokes) >= max_keystrokes:
        keystrokes.pop(0)

def on_release_impl(key):

    if key == keyboard.Key.esc:
        return False
    
    if is_signal_key(key):
        on_signal(key)
        return True
    
    record_keystroke(key)

def on_release(key):
    try:
        return on_release_impl(key)
    except Exception as e:
        logging.error(f"Error: {e}")
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
    except Exception as e:
        logging.error(f"Error: {e}")
