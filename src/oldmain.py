# import time
# import pynput
# from threading import Lock
# import logging
# import colorlog
# import sys

# lock = Lock()
# listen_mode = "listening"
# do_type = True
# type_delay = 0.3
# last_caps_lock_press_time = 0
# double_press_interval = 500  # seconds
# pressed_keys_since_whitespace = [] # Step 1: Initialize the variable to store pressed keys
# keyboard = pynput.keyboard.Controller()
# last_pressed_keys = []

# def setup_logger():
#     logging.basicConfig(level=logging.INFO)

#     logger = logging.getLogger(__name__)
#     stdout = colorlog.StreamHandler(stream=sys.stdout)
#     fmt = colorlog.ColoredFormatter(
#         "%(name)s: %(white)s%(asctime)s%(reset)s | %(log_color)s%(levelname)s%(reset)s | %(blue)s%(filename)s:%(lineno)s%(reset)s | %(process)d >>> %(log_color)s%(message)s%(reset)s"
#     )
#     stdout.setLevel(logging.INFO)
#     stdout.setFormatter(fmt)
#     logger.addHandler(stdout)

#     fileHandler = logging.FileHandler("taptap.log")
#     fmt = logging.Formatter(
#         "%(name)s: %(asctime)s | %(levelname)s | %(filename)s%(lineno)s | %(process)d >>> %(message)s"
#     )
#     fileHandler.setFormatter(fmt)
#     fileHandler.setLevel(logging.INFO)
#     logger.addHandler(fileHandler)

# def is_escape(key):
#     return key == pynput.keyboard.Key.esc

# def is_signal(key):
#     return key == pynput.keyboard.Key.caps_lock

# def milliseconds_since_last_signal(last_caps_lock_press_time):
#     interval = (time.time() - last_caps_lock_press_time) * 1000
#     return int(interval)

# def switch_layout():
#     keyboard.press(pynput.keyboard.Key.ctrl)
#     keyboard.press(pynput.keyboard.Key.shift)
#     keyboard.press(pynput.keyboard.Key.alt)
#     keyboard.press(pynput.keyboard.Key.space)
#     keyboard.release(pynput.keyboard.Key.space)
#     keyboard.release(pynput.keyboard.Key.alt)
#     keyboard.release(pynput.keyboard.Key.shift)
#     keyboard.release(pynput.keyboard.Key.ctrl)

# def clear_signal_sequence():
#     global pressed_keys_since_whitespace, last_pressed_keys
#     while len(pressed_keys_since_whitespace) > 0:
#         last_one = pressed_keys_since_whitespace[-1]
#         if last_one == pynput.keyboard.Key.space \
#         or last_one == pynput.keyboard.Key.caps_lock \
#         or last_one == pynput.keyboard.Key.enter \
#         or last_one == pynput.keyboard.Key.backspace \
#         or last_one == pynput.keyboard.Key.ctrl \
#         or last_one == pynput.keyboard.Key.shift \
#         or last_one == pynput.keyboard.Key.alt_l \
#         or last_one == pynput.keyboard.Key.alt_r:
#             pressed_keys_since_whitespace.pop()
#         else:
#             break

#     while len(last_pressed_keys) > 0:
#         last_one = last_pressed_keys[-1]
#         if last_one == pynput.keyboard.Key.space \
#         or last_one == pynput.keyboard.Key.caps_lock \
#         or last_one == pynput.keyboard.Key.enter \
#         or last_one == pynput.keyboard.Key.backspace \
#         or last_one == pynput.keyboard.Key.ctrl \
#         or last_one == pynput.keyboard.Key.shift \
#         or last_one == pynput.keyboard.Key.alt_l \
#         or last_one == pynput.keyboard.Key.alt_r:
#             last_pressed_keys.pop()
#         else:
#             break
    

# def clear_switch_sequence():
#     global pressed_keys_since_whitespace
#     if len(last_pressed_keys) > 4:
#         if last_pressed_keys[-1] == pynput.keyboard.Key.space:
#             if last_pressed_keys[-2] == pynput.keyboard.Key.alt_l:
#                 if last_pressed_keys[-3] == pynput.keyboard.Key.shift:
#                     if last_pressed_keys[-4] == pynput.keyboard.Key.ctrl:
#                         last_pressed_keys.pop()
#                         last_pressed_keys.pop()
#                         last_pressed_keys.pop()
#                         last_pressed_keys.pop()

# def type_or_log(key):

#     if not do_type:
#         print('type_or_log: {0}'.format(key))
#         return
    
#     try:
#         keyboard.tap(key)
#         time.sleep(type_delay)
#     except AttributeError:
#         # Handle special keys here if needed
#         pass

# def delete_before_type_in_next_layout():
#     global pressed_keys_since_whitespace
#     for i in pressed_keys_since_whitespace:
#         type_or_log(pynput.keyboard.Key.backspace)

# def type_in_next_layout():
#     global pressed_keys_since_whitesp    
#     for i in pressed_keys_since_whitespace:
#         type_or_log(i)

# def on_signal(key):
#     global last_caps_lock_press_time, pressed_keys_since_whitespace, listen_mode # Include the new global variable
    
#     if last_caps_lock_press_time == 0:
#         last_caps_lock_press_time = time.time()
#         return
        
#     if len(pressed_keys_since_whitespace) == 0:
#         last_caps_lock_press_time = time.time()
#         return

#     current_interval = milliseconds_since_last_signal(last_caps_lock_press_time)
#     if current_interval > double_press_interval:
#         last_caps_lock_press_time = time.time()
#         return

#     if last_caps_lock_press_time != 0 and current_interval < double_press_interval:
#         last_caps_lock_press_time = time.time()
#         listen_mode = "processing"
#         switch_layout()
#         clear_signal_sequence()
#         delete_before_type_in_next_layout()
#         clear_signal_sequence()
#         type_in_next_layout()
#         listen_mode = "listening"

#     return True

# def ends_with_control_with_backspaces():
#     """ returnss True if the last 4 keys are ctrl, shift, alt, space """
#     """ followed by a sequence of backspaces """
#     i = len(last_pressed_keys) - 1
#     while i >= 0 and last_pressed_keys[i] == pynput.keyboard.Key.backspace:
#         i -= 1

#     if len(last_pressed_keys) - i > 0:
#         if last_pressed_keys[i] == pynput.keyboard.Key.space:
#             if last_pressed_keys[i-1] == pynput.keyboard.Key.alt_l:
#                 if last_pressed_keys[i-2] == pynput.keyboard.Key.shift:
#                     if last_pressed_keys[i-3] == pynput.keyboard.Key.ctrl:
#                         return True
#     return False

# def is_reset(key):
#     global last_pressed_keys

#     if key == pynput.keyboard.Key.space or \
#     key == pynput.keyboard.Key.enter or \
#     key == pynput.keyboard.Key.backspace:
#         if ends_with_control_with_backspaces():
#             return False
#         else:
#             return True
#     else:
#         return False

# def reset():
#     global pressed_keys_since_whitespace
#     pressed_keys_since_whitespace = []  # Reset the variable
#     print('Reset')

# def collect(key):
#     global pressed_keys_since_whitespace
#     try:
#         pressed_keys_since_whitespace.append(key)
#     except AttributeError:
#         # Handle special keys here if needed
#         pass

# def on_release(key):
#     with lock:
#         global last_caps_lock_press_time, pressed_keys_since_whitespace, listen_mode

#         if listen_mode != "listening":
#             return True

#         if is_escape(key):
#             return False
        
#         if is_signal(key):
#             on_signal(key)
#             return True

#         if is_reset(key):
#             reset()
#             return True
    
#     collect(key)
#     return True

# def on_press(key):
#    with lock:
#         global last_pressed_keys, listen_mode
#         # put the key into last_pressed_keys
#         # drop the oldest key if the length of last_pressed_keys is greater than 10
#         if listen_mode != "listening":
#             return

#         last_pressed_keys.append(key)
#         if len(last_pressed_keys) > 100:
#             last_pressed_keys.pop(0)

# if __name__ == "__main__":
#     setup_logger()
#     logger = logging.getLogger(__name__)
#     logger.info("Starting the program")

#     # Collect events until released
#     with pynput.keyboard.Listener(
#         on_release=on_release,
#         on_press=on_press
#         ) as listener:
#         listener.join()

# # # ...or, in a non-blocking fashion:
# # listener = keyboard.Listener(
# #     on_press=on_press,
# #     on_release=on_release)
# # listener.start()
