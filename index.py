import sys
import os
import data.player as character
cols = 100
lines = 30
player = character.Warrior('name')


def menu_logo():
    print('#' * 100)
    print(' ' * 37, 'Welcome in RPG adventure.')
    print('#' * 100)


def new():
    global player
    option = ''
    while option != 'yes':
        os.system('cls')
        menu_logo()
        print(' ' * 39, 'Hi, tell me your name')
        name = input("> ").capitalize()
        print(' ' * (35-int(len(name)/2)), f'Okey, {name}, now tell me your class')
        print(' ' * 45, 'You can be:')
        print(' ' * 47, 'Warrior')
        character_class = ''
        while character_class not in ['Warrior']:
            character_class = input("> ").capitalize()
        os.system('cls')
        menu_logo()
        text = f'{name}, the {character_class} are you ready to new adventure?'
        print(' ' * (50 - int(len(text)/2)), text)
        option = input("> ").lower()
        if character_class == 'Warrior':
            player = character.Warrior(name)


def load():
    raise NotImplementedError


def title_screen():
    option = ''
    while option not in ['new', 'new game', 'load', 'quit', 'q']:
        menu_logo()
        print(' ' * 42, '.: New Game :.', ' ' * 42)
        print(' ' * 44, '.: Load :.', ' ' * 44)
        print(' ' * 44, '.: Quit :.', ' ' * 44)
        option = input("> ").lower()
        if option == 'new' or option == 'new game':
            new()
            main_game_loop()
        elif option == 'load':
            load()
        elif option == 'quit' or option == 'q':
            sys.exit()
        os.system('cls')

def game_window():
    print('─'*100)
    option = input("> ").lower()

def main_game_loop():
    os.system('cls')
    game_window()

os.system(f'mode con: cols={cols} lines={lines}')
os.system('cls')
title_screen()
