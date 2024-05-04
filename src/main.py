import keyboard
import time

# The last word typed
last_word = ""

# The time the last caps lock was pressed
last_caps_time = 0

def reset_last_word():
    global last_word
    last_word = ""

def check_caps_lock_press(event):
    global last_caps_time
    if time.time() - last_caps_time < 0.5:
        delete_last_word()
        type_translated_word()

def delete_last_word():
    global last_word
    keyboard.send('backspace', repeat=len(last_word))

def type_translated_word():
    print("Type the translated word")

def on_key(event):
    print(event)
    if event.name == 'space':
        print("If the key is space, reset the last word")
        reset_last_word()
        return
    
    if event.name == 'caps lock' and event.event_type == 'down':
        check_caps_lock_press(event)
        return
    
    if event.event_type == 'down':
        print("If the key is down, add the key to the last word")
        add_key_to_last_word(event)

if __name__ == "__main__":    
    # Start listening to keyboard events
    keyboard.hook(on_key)
    print("Listening to keyboard events")
    keyboard.wait()
