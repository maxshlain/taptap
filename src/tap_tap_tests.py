# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
import unittest
from unittest.mock import patch, MagicMock
from pynput import keyboard
from tap_tap import TapTap

class TestTapTap(unittest.TestCase):
    def setUp(self):
        self.tap_tap = TapTap()

    @patch('tap_tap.keyboard.Controller')
    def test_init(self, mock_controller):
        self.assertEqual(self.tap_tap.last_caps_lock_press_time, 0)
        self.assertEqual(self.tap_tap.double_press_interval, 999)
        self.assertEqual(self.tap_tap.max_keystrokes, 999)
        self.assertEqual(self.tap_tap.keystrokes, [])
        self.assertEqual(self.tap_tap.last_word_keystrokes, [])
        # mock_controller.assert_called_once()

    # @patch('tap_tap.keyboard.Controller')
    # @patch('tap_tap.time.sleep')
    # def test_tap_and_delay(self, mock_sleep, mock_controller):
    #     key = keyboard.Key.space
    #     self.tap_tap.tap_and_delay(key)
    #     mock_controller().tap.assert_called_once_with(key)
    #     mock_sleep.assert_called_once_with(0.2)

    # @patch('tap_tap.keyboard.Controller')
    # @patch('tap_tap.TapTap.tap_and_delay')
    # def test_delete_before_type_in_next_layout(self, mock_tap_and_delay, mock_controller):
    #     count = 5
    #     self.tap_tap.delete_before_type_in_next_layout(count)
    #     self.assertEqual(mock_tap_and_delay.call_count, count)

if __name__ == '__main__':
    unittest.main()
