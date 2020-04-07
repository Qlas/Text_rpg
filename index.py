import pygame
import data.player as character
from data.buttons import Button, Text, InputText
from data.map_generator import Map

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
        self.menu = False
        self.game = False
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.all_buttons = pygame.sprite.Group()
        self.all_text = pygame.sprite.Group()
        self.menu = 0
        self.name = ''
        self.character_class = ''
        self.player = character.Warrior(self.name)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.menu = True
                self.game = True
            for button in self.all_buttons:
                button.handle_event(event)

    def main_game(self):
        self.all_buttons = pygame.sprite.Group()
        self.all_text = pygame.sprite.Group()
        self.game_window()
        while not self.game:
            self.handle_events()
            self.run_logic()
            self.draw()

    def game_window(self):
        stats_height = 300
        name = Text(text=f'Name: {self.player.name}', color=(255, 255, 255),
                    width=650, height=stats_height, font=pygame.font.SysFont('Arial', 15), align='left')
        char_class = Text(text=f'Class: {self.player.__str__()}', color=(255, 255, 255),
                          width=650, height=stats_height + 20, font=pygame.font.SysFont('Arial', 15), align='left')
        strength = Text(text=f'Strength: {self.player.strength}', color=(255, 255, 255),
                        width=650, height=stats_height + 40, font=pygame.font.SysFont('Arial', 15), align='left')
        dexterity = Text(text=f'Dexterity: {self.player.dexterity}', color=(255, 255, 255),
                         width=650, height=stats_height + 60, font=pygame.font.SysFont('Arial', 15), align='left')
        intel = Text(text=f'Intelligence: {self.player.intelligence}', color=(255, 255, 255),
                     width=650, height=stats_height + 80, font=pygame.font.SysFont('Arial', 15), align='left')
        lvl = Text(text=f'Lvl: {self.player.lvl}', color=(255, 255, 255),
                   width=650, height=stats_height + 100, font=pygame.font.SysFont('Arial', 15), align='left')
        exp = Text(text=f'Exp: {self.player.exp}', color=(255, 255, 255),
                   width=650, height=stats_height + 120, font=pygame.font.SysFont('Arial', 15), align='left')
        exp_to_lvl = Text(text=f'Next lvl: {self.player.exp_to_next_lvl - self.player.exp}', color=(255, 255, 255),
                          width=650, height=stats_height + 140, font=pygame.font.SysFont('Arial', 15), align='left')
        eq = Button(
            650, 500, 150, 50, self.eq,
            FONT, pygame.Surface((100, 32)), pygame.Surface((100, 32)),
            pygame.Surface((100, 32)), 'EQ', (255, 255, 255))

        if self.player.location == 'Village':
            merchant = Button(
                50, 50, 150, 50, self.merchant,
                pygame.font.SysFont('Arial', 15), pygame.Surface((100, 32)), pygame.Surface((100, 32)),
                pygame.Surface((100, 32)), 'Merchant', (255, 255, 255))
            blacksmith = Button(
                400, 50, 150, 50, self.blacksmith,
                pygame.font.SysFont('Arial', 15), pygame.Surface((100, 32)), pygame.Surface((100, 32)),
                pygame.Surface((100, 32)), 'Blacksmith', (255, 255, 255))
            dungeon = Button(
                200, 200, 150, 50, self.dungeon,
                pygame.font.SysFont('Arial', 15), pygame.Surface((100, 32)), pygame.Surface((100, 32)),
                pygame.Surface((100, 32)), 'Dungeon', (255, 255, 255))
            self.all_buttons.add(merchant, dungeon, blacksmith)

        self.all_buttons.add(eq)
        self.all_text.add(name, char_class, strength, dexterity, intel, lvl, exp, exp_to_lvl)

    def merchant(self):
        pass

    def blacksmith(self):
        pass

    def dungeon_map(self):
        player_loc = Text(text=f'Player', color=(255, 255, 255),
                          width=300, height=200, font=pygame.font.SysFont('Arial', 15))
        self.all_text.add(player_loc)
        if self.player.location.neighbor['N'] is not None:
            north = Text(text=f'{self.player.location.neighbor["N"]}', color=(255, 255, 255),
                         width=300, height=150, font=pygame.font.SysFont('Arial', 15))
            self.all_text.add(north)
        if self.player.location.neighbor['S'] is not None:
            south = Text(text=f'{self.player.location.neighbor["S"]}', color=(255, 255, 255),
                         width=300, height=250, font=pygame.font.SysFont('Arial', 15))
            self.all_text.add(south)
        if self.player.location.neighbor['W'] is not None:
            west = Text(text=f'{self.player.location.neighbor["W"]}', color=(255, 255, 255),
                        width=200, height=200, font=pygame.font.SysFont('Arial', 15))
            self.all_text.add(west)
        if self.player.location.neighbor['E'] is not None:
            east = Text(text=f'{self.player.location.neighbor["E"]}', color=(255, 255, 255),
                        width=400, height=200, font=pygame.font.SysFont('Arial', 15))
            self.all_text.add(east)
        move_north = Button(
            100, 450, 50, 50, self.move_north,
            pygame.font.SysFont('Arial', 15), pygame.Surface((100, 32)), pygame.Surface((100, 32)),
            pygame.Surface((100, 32)), 'North', (255, 255, 255))
        move_south = Button(
            100, 500, 50, 50, self.move_south,
            pygame.font.SysFont('Arial', 15), pygame.Surface((100, 32)), pygame.Surface((100, 32)),
            pygame.Surface((100, 32)), 'South', (255, 255, 255))
        move_west = Button(
            50, 500, 50, 50, self.move_west,
            pygame.font.SysFont('Arial', 15), pygame.Surface((100, 32)), pygame.Surface((100, 32)),
            pygame.Surface((100, 32)), 'West', (255, 255, 255))
        move_east = Button(
            150, 500, 50, 50, self.move_east,
            pygame.font.SysFont('Arial', 15), pygame.Surface((100, 32)), pygame.Surface((100, 32)),
            pygame.Surface((100, 32)), 'East', (255, 255, 255))

        self.all_buttons.add(move_north, move_south, move_west, move_east)

    def move_north(self):
        if self.player.location.neighbor['N'] is not None:
            self.all_buttons = pygame.sprite.Group()
            self.all_text = pygame.sprite.Group()
            self.player.location = self.player.location.neighbor['N']
            self.player.location.visited = True
            self.dungeon_map()

    def move_south(self):
        if self.player.location.neighbor['S'] is not None:
            self.all_buttons = pygame.sprite.Group()
            self.all_text = pygame.sprite.Group()
            self.player.location = self.player.location.neighbor['S']
            self.player.location.visited = True
            self.dungeon_map()

    def move_west(self):
        if self.player.location.neighbor['W'] is not None:
            self.all_buttons = pygame.sprite.Group()
            self.all_text = pygame.sprite.Group()
            self.player.location = self.player.location.neighbor['W']
            self.player.location.visited = True
            self.dungeon_map()

    def move_east(self):
        if self.player.location.neighbor['E'] is not None:
            self.all_buttons = pygame.sprite.Group()
            self.all_text = pygame.sprite.Group()
            self.player.location = self.player.location.neighbor['E']
            self.player.location.visited = True
            self.dungeon_map()

    def dungeon(self):
        self.all_buttons = pygame.sprite.Group()
        self.all_text = pygame.sprite.Group()
        tiles = 10
        dung = Map(tiles)
        self.player.location = dung.rooms[tiles][tiles]
        self.player.location.visited = True
        self.game_window()

        self.dungeon_map()

    def eq(self):
        pass

    def logo(self):
        logo_text = Text(text='Welcome in RPG adventure.', color=(255, 255, 255), width=800 / 2, height=100, font=FONT)
        self.all_text.add(logo_text)

    def input_button(self, name):
        self.name = name

    def create_character_show(self):
        self.all_buttons = pygame.sprite.Group()
        back_button = Button(
            50, 500, 150, 65, self.back,
            FONT, IMAGE_NORMAL, IMAGE_HOVER, IMAGE_DOWN, 'Back', (255, 255, 255), )
        start_button = Button(
            600, 500, 150, 65, self.start_game,
            FONT, IMAGE_NORMAL, IMAGE_HOVER, IMAGE_DOWN, 'Start', (255, 255, 255), )
        text_name = Text(text='Name: ', color=(255, 255, 255), width=100, height=200, font=FONT)
        input_button = InputText(text=self.name, color=(255, 255, 255), width=150, font=FONT,
                                 height=177, callback=self.input_button)
        warrior_button = Button(
            50, 300, 150, 65, self.warrior,
            FONT, IMAGE_NORMAL, IMAGE_HOVER, IMAGE_DOWN, 'Warrior', (255, 255, 255))
        class_text = Text(text=f'Class: {self.character_class}',
                          color=(255, 255, 255), width=45, height=230, font=FONT, align='left')
        self.all_buttons.add(back_button, start_button, input_button, warrior_button)
        self.all_text.add(text_name, class_text)

    def start_game(self):
        if self.name != '' and self.character_class != '':
            self.player = character.Warrior(self.name)
            self.menu = True

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
            FONT, IMAGE_NORMAL, IMAGE_HOVER, IMAGE_DOWN, 'Load', (255, 255, 255), )
        quit_button = Button(
            320, 400, 170, 65, self.quit_game,
            FONT, IMAGE_NORMAL, IMAGE_HOVER, IMAGE_DOWN, 'Quit', (255, 255, 255))
        self.all_buttons.add(new_game_button, load_button, quit_button)

    def main_menu(self):
        self.main_menu_show()
        self.logo()
        while not self.menu:
            self.handle_events()
            self.run_logic()
            self.draw()

    def new_game(self):
        self.create_character_show()

    def load(self):
        pass

    def quit_game(self):
        self.menu = True
        self.game = True

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
    g.main_game()
    pygame.quit()
