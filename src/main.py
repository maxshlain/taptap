import time
import pynput

last_caps_lock_press_time = 0
double_press_interval = 0.5  # seconds
pressed_keys_since_whitespace = [] # Step 1: Initialize the variable to store pressed keys
keyboard = pynput.keyboard.Controller()

def on_release(key):
    global last_caps_lock_press_time, pressed_keys_since_whitespace  # Include the new global variable
    
    if key == pynput.keyboard.Key.esc:
        return False
    
    if key == pynput.keyboard.Key.caps_lock:

        if last_caps_lock_press_time == 0:
            last_caps_lock_press_time = time.time()
            return True
        
        if len(pressed_keys_since_whitespace) == 0:
            last_caps_lock_press_time = time.time()
            return True

        current_interval = time.time() - last_caps_lock_press_time
        if current_interval > double_press_interval:
            last_caps_lock_press_time = time.time()
            return True

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

    # Step 2: Reset pressed_keys_since_whitespace on whitespace
    if key == pynput.keyboard.Key.space or key == pynput.keyboard.Key.enter:
        print(f"Keys since last whitespace: {pressed_keys_since_whitespace}")
        pressed_keys_since_whitespace = []  # Reset the variable
    else:
        # Step 3: Append non-whitespace keys to pressed_keys_since_whitespace
        try:
            pressed_keys_since_whitespace.append(key)
        except AttributeError:
            # Handle special keys here if needed
            pass

    return True

# Collect events until released
with pynput.keyboard.Listener(on_release=on_release) as listener:
    listener.join()

# # ...or, in a non-blocking fashion:
# listener = keyboard.Listener(
#     on_press=on_press,
#     on_release=on_release)
# listener.start()
