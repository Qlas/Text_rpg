import pygame
import data.player as character
from data.buttons import Button, Text, InputText

screenSize = (800, 600)
resolution = pygame.display.set_mode(screenSize)
pygame.init()


FONT = pygame.font.SysFont('Comic Sans MS', 32)
IMAGE_NORMAL = pygame.Surface((100, 32))
IMAGE_NORMAL.fill(pygame.Color('dodgerblue1'))
IMAGE_HOVER = pygame.Surface((100, 32))
IMAGE_HOVER.fill(pygame.Color('lightskyblue'))
IMAGE_DOWN = pygame.Surface((100, 32))
IMAGE_DOWN.fill(pygame.Color('aquamarine1'))


class Game:
    def __init__(self, screen):
        self.done = False
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.all_buttons = pygame.sprite.Group()
        self.all_text = pygame.sprite.Group()
        self.menu = 0
        self.name = ''
        self.character_class = ''
        self.player = character.Player

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            for button in self.all_buttons:
                button.handle_event(event)

    def logo(self):
        logo_text = Text(text='Welcome in RPG adventure.', color=(255, 255, 255), width=800/2, height=100, font=FONT)
        self.all_text.add(logo_text)

    def input_button(self, name):
        self.name = name

    def create_character_show(self):
        self.all_buttons = pygame.sprite.Group()
        back_button = Button(
            50, 500, 150, 65, self.back,
            FONT, IMAGE_NORMAL, IMAGE_HOVER, IMAGE_DOWN, 'Back', (255, 255, 255),)
        start_button = Button(
            600, 500, 150, 65, self.start_game,
            FONT, IMAGE_NORMAL, IMAGE_HOVER, IMAGE_DOWN, 'Start', (255, 255, 255),)
        text_name = Text(text='Name: ', color=(255, 255, 255), width=100, height=200, font=FONT)
        input_button = InputText(text=self.name, color=(255, 255, 255), width=150, font=FONT,
                                 height=177, callback=self.input_button)
        warrior_button = Button(
            50, 300, 150, 65, self.warrior,
            FONT, IMAGE_NORMAL, IMAGE_HOVER, IMAGE_DOWN, 'Warrior', (255, 255, 255),)
        class_text = Text(text=f'Class: {self.character_class}', color=(255, 255, 255), width=200, height=260, font=FONT)
        self.all_buttons.add(back_button, start_button, input_button, warrior_button)
        self.all_text.add(text_name, class_text)

    def start_game(self):
        if self.name != '' and self.character_class != '':
            self.player = character.Warrior(self.name)
            self.done = True

    def warrior(self):
        self.character_class = 'Warrior'
        self.create_character_show()

    def back(self):
        self.all_buttons = pygame.sprite.Group()
        self.all_text = pygame.sprite.Group()
        self.main_menu_show()

    def main_menu_show(self):
        self.logo()
        new_game_button = Button(
            320, 200, 170, 65, self.new_game,
            FONT, IMAGE_NORMAL, IMAGE_HOVER, IMAGE_DOWN, 'New Game', (255, 255, 255))
        load_button = Button(
            320, 300, 170, 65, self.load,
            FONT, IMAGE_NORMAL, IMAGE_HOVER, IMAGE_DOWN,  'Load', (255, 255, 255),)
        quit_button = Button(
            320, 400, 170, 65, self.quit_game,
            FONT, IMAGE_NORMAL, IMAGE_HOVER, IMAGE_DOWN, 'Quit', (255, 255, 255))
        self.all_buttons.add(new_game_button, load_button, quit_button)

    def main_menu(self):
        self.main_menu_show()
        self.logo()
        while not self.done:
            self.handle_events()
            self.run_logic()
            self.draw()

    def new_game(self):
        self.create_character_show()

    def load(self):
        pass

    def quit_game(self):
        self.done = True

    def run_logic(self):
        self.all_buttons.update()
        pygame.display.update()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.all_buttons.draw(self.screen)
        self.all_text.draw(self.screen)


if __name__ == '__main__':
    pygame.init()
    g = Game(resolution)
    g.main_menu()
    pygame.quit()
