import time
import pynput

last_caps_lock_press_time = 0
double_press_interval = 500  # seconds
pressed_keys_since_whitespace = [] # Step 1: Initialize the variable to store pressed keys
keyboard = pynput.keyboard.Controller()

def is_escape(key):
    return key == pynput.keyboard.Key.esc

def is_signal(key):
    return key == pynput.keyboard.Key.caps_lock

def milliseconds_since_last_signal(last_caps_lock_press_time):
    interval = (time.time() - last_caps_lock_press_time) * 1000
    return int(interval)

def on_signal(key):
    global last_caps_lock_press_time, pressed_keys_since_whitespace  # Include the new global variable
    
    if last_caps_lock_press_time == 0:
        last_caps_lock_press_time = time.time()
        return
        
    if len(pressed_keys_since_whitespace) == 0:
        last_caps_lock_press_time = time.time()
        return

    current_interval = milliseconds_since_last_signal(last_caps_lock_press_time)
    print(f"Current interval: {current_interval}")
    if current_interval > double_press_interval:
        last_caps_lock_press_time = time.time()
        return

    if last_caps_lock_press_time != 0 and current_interval < double_press_interval:
        last_caps_lock_press_time = time.time()  # Reset to avoid triple press detection
        print(f"Double {current_interval} Caps lock pressed")
        print(f"Keys since last whitespace: {pressed_keys_since_whitespace}")
        for i in pressed_keys_since_whitespace:
            try:
                if i.char:
                    keyboard.type(i.char)
            except AttributeError:
                # Handle special keys here if needed
                pass
        pressed_keys_since_whitespace = []
    return True

def is_reset(key):
    return key == pynput.keyboard.Key.space or \
    key == pynput.keyboard.Key.enter or \
    key == pynput.keyboard.Key.backspace

def reset():
    global pressed_keys_since_whitespace
    print(f"Keys since last whitespace: {pressed_keys_since_whitespace}")
    pressed_keys_since_whitespace = []  # Reset the variable

def collect(key):
    global pressed_keys_since_whitespace
    try:
        pressed_keys_since_whitespace.append(key)
    except AttributeError:
        # Handle special keys here if needed
        pass

def on_release(key):
    global last_caps_lock_press_time, pressed_keys_since_whitespace  # Include the new global variable
    
    if is_escape(key):
        return False
    
    if is_signal(key):
        on_signal(key)
        return True

    if is_reset(key):
        reset()
        return True
    
    collect(key)
    return True

# Collect events until released
with pynput.keyboard.Listener(on_release=on_release) as listener:
    listener.join()

# # ...or, in a non-blocking fashion:
# listener = keyboard.Listener(
#     on_press=on_press,
#     on_release=on_release)
# listener.start()
