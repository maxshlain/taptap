from pynput import keyboard
import time

last_caps_lock_press_time = 0
double_press_interval = 0.5  # seconds

def on_release(key):
    global last_caps_lock_press_time
    if key == keyboard.Key.esc:
        # Stop listener
        return False
    if key == keyboard.Key.caps_lock:
        current_time = time.time()

        if last_caps_lock_press_time == 0:
            last_caps_lock_press_time = current_time
            return True

        current_interval = current_time - last_caps_lock_press_time
        if current_interval > double_press_interval:
            last_caps_lock_press_time = current_time
            return True

        if last_caps_lock_press_time != 0 and current_interval < double_press_interval:
            print(f"Double {current_interval} Caps lock pressed")
            last_caps_lock_press_time = current_time # Reset to avoid triple press detection
        return True

    # print('{0} released'.format(key))

# Collect events until released
with keyboard.Listener(
        on_release=on_release) as listener:
    listener.join()

# # ...or, in a non-blocking fashion:
# listener = keyboard.Listener(
#     on_press=on_press,
#     on_release=on_release)
# listener.start()
