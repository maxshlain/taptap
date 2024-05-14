from pynput import keyboard 
import logging
import time

class TapTap:
    def __init__(self):
        self.last_caps_lock_press_time = 0
        self.double_press_interval = 999  # milliseconds
        self.max_keystrokes = 999
        self.keystrokes = []
        self.last_word_keystrokes = []
        self.keyboard_controller = keyboard.Controller()

    def tap_and_delay(self, key):
        self.keyboard_controller.tap(key)
        time.sleep(0.2)

    def delete_before_type_in_next_layout(self, count):
        for i in range(count):
            self.tap_and_delay(keyboard.Key.backspace)
    # end def

    def type_in_next_layout(self, word):
        for key in word:
            self.tap_and_delay(key)
    # end def

    def switch_layout(self):
        self.keyboard_controller.press(keyboard.Key.ctrl)
        self.keyboard_controller.press(keyboard.Key.shift)
        self.keyboard_controller.press(keyboard.Key.alt)
        self.keyboard_controller.press(keyboard.Key.space)
        self.keyboard_controller.release(keyboard.Key.space)
        self.keyboard_controller.release(keyboard.Key.alt)
        self.keyboard_controller.release(keyboard.Key.shift)
        self.keyboard_controller.release(keyboard.Key.ctrl)
    # end def

    def is_signal_key(self, key):
        return key == keyboard.Key.ctrl_l
    # end def

    def milliseconds_since_last_signal(self, last_caps_lock_press_time):
        interval = (time.time() - last_caps_lock_press_time) * 1000
        return int(interval)
    # end def

    def on_signal(self, key):
        if self.last_caps_lock_press_time == 0:
            self.last_caps_lock_press_time = time.time()
            return

        current_interval = self.milliseconds_since_last_signal(self.last_caps_lock_press_time)
        if current_interval > self.double_press_interval:
            self.last_caps_lock_press_time = time.time()
            return

        if self.last_caps_lock_press_time != 0 and current_interval < self.double_press_interval:
            self.last_caps_lock_press_time = time.time()
            last_word = self.get_last_word()
            self.switch_layout()
            self.delete_before_type_in_next_layout(len(last_word))
            self.type_in_next_layout(last_word)
    # end def

    def get_char(self, key):
        try:
            return key.char
        except AttributeError:
            return None
    # end def

    def get_last_word(self):

        if len(self.keystrokes) < 1:
            return

        last_word_text = ''
        i = len(self.keystrokes) - 1
        first_whitespace_index = -1
        non_space_seen = False
        while i >= 0:
            next_key = self.keystrokes[i]
            i -= 1

            next_char = self.get_char(next_key)
            if next_char:
                non_space_seen = True

            if next_key == keyboard.Key.space or next_key == keyboard.Key.enter:
                if non_space_seen and first_whitespace_index == -1:
                    first_whitespace_index = i + 1
        # end while

        result_keystrokes = []
        if first_whitespace_index == -1:
            for keystroke in self.keystrokes:
                next_char = self.get_char(keystroke)
                if next_char:
                    last_word_text += self.get_char(keystroke)
                    result_keystrokes.append(keystroke)
            return result_keystrokes

        i = first_whitespace_index
        while i < len(self.keystrokes):
            next_key = self.keystrokes[i]
            i += 1
            next_char = self.get_char(next_key)
            if next_char:
                last_word_text += self.get_char(next_key)
                result_keystrokes.append(next_key)
        return result_keystrokes
    # end def

    def record_keystroke(self, key):
        self.keystrokes.append(key)
        if len(self.keystrokes) >= self.max_keystrokes:
            self.keystrokes.pop(0)
    # end def

    def on_release_impl(self, key):

        if key == keyboard.Key.esc:
            return False

        if self.is_signal_key(key):
            self.on_signal(key)
            return True

        self.record_keystroke(key)
        return True
    # end def
# end class
