import keyboard
import time

# # A dictionary to map English letters to Russian
# eng_to_rus = {
#     'a': 'ф', 'b': 'и', 'c': 'с', 'd': 'в', 'e': 'у', 'f': 'а', 'g': 'п', 'h': 'р', 'i': 'ш', 'j': 'о', 'k': 'л', 'l': 'д', 'm': 'ь', 'n': 'т', 'o': 'щ', 'p': 'з', 'q': 'й', 'r': 'к', 's': 'ы', 't': 'е', 'u': 'г', 'v': 'м', 'w': 'ц', 'x': 'ч', 'y': 'н', 'z': 'я',
#     'A': 'Ф', 'B': 'И', 'C': 'С', 'D': 'В', 'E': 'У', 'F': 'А', 'G': 'П', 'H': 'Р', 'I': 'Ш', 'J': 'О', 'K': 'Л', 'L': 'Д', 'M': 'Ь', 'N': 'Т', 'O': 'Щ', 'P': 'З', 'Q': 'Й', 'R': 'К', 'S': 'Ы', 'T': 'Е', 'U': 'Г', 'V': 'М', 'W': 'Ц', 'X': 'Ч', 'Y': 'Н', 'Z': 'Я'
# }

# The last word typed
last_word = ""

# The time the last caps lock was pressed
last_caps_time = 0

def on_key(event):
    global last_word, last_caps_time
    if event.name == 'space':
        print("If the key is space, reset the last word")
        last_word = ""
    elif event.name == 'caps lock' and event.event_type == 'down':
        print("If caps lock is pressed twice quickly, translate the last word")
        if time.time() - last_caps_time < 0.5:
            print("Delete the last word")
            keyboard.send('backspace', repeat=len(last_word))
            print("Type the translated word")
            for char in last_word:
                if char in eng_to_rus:
                    keyboard.write(eng_to_rus[char])
                else:
                    keyboard.write(char)
            last_word = ""
        last_caps_time = time.time()
    elif event.event_type == 'down':
    # else:
        # If the key is alphanumeric, add it to the last word
        print("If the key is alphanumeric, add it to the last word")
        print(f"The key is {event.scan_code}")
        # last_word += event.name
        print("The last word is", last_word)

# Start listening to keyboard events
keyboard.hook(on_key)
print("Listening to keyboard events")
keyboard.wait()
