from scripts.core.settings import CONSOLE_COMMAND_WORD
from scripts.core.console.consoleCommand import ConsoleCommand

import pygame as pg

class ConsoleHandler:
    def __init__(self, appInstance):
        self.app = appInstance

        self.available_commands = []

        self.console_state = 0

    def show_console(self):
        self.console_state = 1
        pg.key.start_text_input()

    def hide_console(self):
        self.console_state = 0
        pg.key.stop_text_input()

    def toggle_console(self):
        if self.console_state:
            self.hide_console()
        else:
            self.show_console()

    def get_console_state(self):
        return self.console_state

    def parse_console_input(self, input:str):
        words = input.strip().split(" ")

        if words[0][0] == CONSOLE_COMMAND_WORD:
            words[0] = words[0][1:] # this is weird-

            self.execute_console_input(words)

        else:
            self.print_to_console(input.strip())

    def execute_console_input(self, command_words:list[str]):
        pass

    def print_to_console(self, word:str):
        pass

    def register_command(self, command:ConsoleCommand):
        command_name = command.name
        command_desc = command.desc

        if command_name in self.available_commands:
            print(f"{__name__}: Console command {command_name} <{command_desc}> is already registered! Consider using a different name")

        else:
            self.available_commands.append(command)