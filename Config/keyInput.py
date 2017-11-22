import sys

from Config import config

def key_input():
    while True:
        console_input = input()
        if console_input == "s":
            config.is_input_word = True
        elif console_input == "e":
            config.is_input_word = False
            config.finish_input_word = True
        elif console_input == "o":
            config.is_calibration = True
        elif console_input == "f":
            sys.exit()
        elif console_input != config.console_input_number:
            config.console_input_number = console_input
            print("c =", config.console_input_number)
        else:
            print("else")
