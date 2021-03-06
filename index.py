import pygame
import data.player as character
from data.sprites import Button, Text, InputText
from data.map_generator import Map
import data.sprites as btn
import pickle
import numpy as np
import colorsys
import data.functions

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

    def player_stats(self):
        font = pygame.font.SysFont('Arial', 15)
        stats_height = 10
        stats_width = 650

        self.all_text.add(btn.Background('images/board_stone.png', [620, 0], 180, 200))
        bar_percentage = self.player.stats['hp'] / self.player.stats['max_hp']
        h, s, v = 0.33 * bar_percentage, 1, 1
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        self.all_text.add(btn.Bars((int(255 * r), int(255 * g), int(255 * b)), [650, 0], 100, 10))

        name = Text(x=stats_width, y=stats_height,
                    text=f'Name: {self.player.name}', font=font, align='left')
        char_class = Text(x=stats_width, y=stats_height + 20,
                          text=f'Class: {self.player.__str__()}', font=font, align='left')
        strength = Text(x=stats_width, y=stats_height + 40,
                        text=f'Strength: {self.player.stats["strength"]}', font=font, align='left')
        dexterity = Text(x=stats_width, y=stats_height + 60,
                         text=f'Dexterity: {self.player.stats["dexterity"]}', font=font, align='left')
        intel = Text(x=stats_width, y=stats_height + 80,
                     text=f'Intelligence: {self.player.stats["intelligence"]}', font=font, align='left')
        lvl = Text(x=stats_width, y=stats_height + 100,
                   text=f'Lvl: {self.player.stats["lvl"]}', color=(255, 255, 255), font=font, align='left')
        exp = Text(x=stats_width, y=stats_height + 120,
                   text=f'Exp: {self.player.exp}', color=(255, 255, 255), font=font, align='left')
        exp_to_lvl = Text(x=stats_width, y=stats_height + 140,
                          text=f'Next lvl: {self.player.exp_to_next_lvl - self.player.exp}', font=font, align='left')
        self.all_text.add(name, char_class, strength, dexterity, intel, lvl, exp, exp_to_lvl)

    def game_window(self):
        self.player_stats()
        eq = Button(
            650, 500, 150, 50, self.eq,
            FONT, pygame.Surface((100, 32)), pygame.Surface((100, 32)),
            pygame.Surface((100, 32)), 'EQ', (255, 255, 255))

        if self.player.location == 'Village':

            background = btn.Background('images/village.jpg', [0, 0], 800, 600)
            self.all_text.add(background)

            merchant = Button(
                80, 480, 150, 50, self.merchant,
                pygame.font.SysFont('Arial', 15), text='Merchant', text_color=(255, 255, 255), image='')
            blacksmith = Button(
                560, 370, 150, 50, self.blacksmith,
                pygame.font.SysFont('Arial', 15), text='Blacksmith', text_color=(255, 255, 255), image='')
            dungeon = Button(
                540, 160, 130, 110, self.dungeon,
                pygame.font.SysFont('Arial', 15), text='Dungeon', text_color=(255, 255, 255), image='')
            self.all_buttons.add(merchant, dungeon, blacksmith)

        self.all_buttons.add(eq)

    def merchant(self):
        pass

    def blacksmith(self):
        pass

    def dungeon_map(self):
        room_pos = [680, 5]
        room_pos_start = [680, 5]
        map_tiles = btn.get_map_image()
        maps = pygame.sprite.Group()
        center_tile = list(zip(np.where(self.player.dung.rooms == self.player.location)))
        map_size = 3
        background = btn.Background('images/dungeon_background.jpg', [0, 0], 800, 600)
        map_background = btn.Background('images/board_stone.png', [room_pos[0]-7, room_pos[1]-5], 125, 94)
        self.all_text.add(background, map_background)
        for room_x in range(int(center_tile[0][0] - map_size), int(center_tile[0][0] + map_size + 1)):
            if room_x >= len(self.player.dung.rooms):
                room_x = len(self.player.dung.rooms) - 1
            for room_y in range(int(center_tile[1][0] - map_size), int(center_tile[1][0] + map_size + 1)):
                if room_y >= len(self.player.dung.rooms[0]):
                    room_y = len(self.player.dung.rooms[0]) - 1
                if self.player.dung.rooms[room_x, room_y] is None:
                    btn.MiniMap(map_tiles[0], room_pos, maps, 16, 12)
                else:
                    neighbors = []
                    for neighbor in self.player.dung.rooms[room_x, room_y].neighbor.items():
                        if neighbor[1] is not None:
                            neighbors.append(neighbor[0])
                        if not self.player.dung.rooms[room_x, room_y].visited:
                            btn.MiniMap(map_tiles[0], room_pos, maps, 16, 12)
                        elif neighbors == ['N', 'S', 'W', 'E']:
                            btn.MiniMap(map_tiles[1], room_pos, maps, 16, 12)
                        elif neighbors == ['N', 'S', 'W']:
                            btn.MiniMap(map_tiles[16], room_pos, maps, 16, 12)
                        elif neighbors == ['N', 'S', 'E']:
                            btn.MiniMap(map_tiles[14], room_pos, maps, 16, 12)
                        elif neighbors == ['N', 'W', 'E']:
                            btn.MiniMap(map_tiles[13], room_pos, maps, 16, 12)
                        elif neighbors == ['S', 'W', 'E']:
                            btn.MiniMap(map_tiles[15], room_pos, maps, 16, 12)
                        elif neighbors == ['N', 'S']:
                            btn.MiniMap(map_tiles[8], room_pos, maps, 16, 12)
                        elif neighbors == ['N', 'W']:
                            btn.MiniMap(map_tiles[9], room_pos, maps, 16, 12)
                        elif neighbors == ['N', 'E']:
                            btn.MiniMap(map_tiles[7], room_pos, maps, 16, 12)
                        elif neighbors == ['S', 'W']:
                            btn.MiniMap(map_tiles[12], room_pos, maps, 16, 12)
                        elif neighbors == ['S', 'E']:
                            btn.MiniMap(map_tiles[10], room_pos, maps, 16, 12)
                        elif neighbors == ['W', 'E']:
                            btn.MiniMap(map_tiles[11], room_pos, maps, 16, 12)
                        elif neighbors == ['N']:
                            btn.MiniMap(map_tiles[3], room_pos, maps, 16, 12)
                        elif neighbors == ['S']:
                            btn.MiniMap(map_tiles[5], room_pos, maps, 16, 12)
                        elif neighbors == ['W']:
                            btn.MiniMap(map_tiles[6], room_pos, maps, 16, 12)
                        elif neighbors == ['E']:
                            btn.MiniMap(map_tiles[4], room_pos, maps, 16, 12)
                        if room_x == center_tile[0][0] and room_y == center_tile[1][0]:
                            btn.MiniMap(map_tiles[18], room_pos, maps, 16, 12)

                room_pos[0] += 16
            room_pos[1] += 12
            room_pos[0] = room_pos_start[0]
        self.all_text.add(maps)

        # self.player_stats()

        bottom_background = btn.Background('images/board_stone.png', [-50, 430], 900, 250)
        self.all_text.add(bottom_background)

        move_north = Button(
            100, 460, 50, 50, self.move_north,
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

    def fight(self):
        pass

    def treasure(self):
        item = data.functions.generate_random_item(self.player)
        print(item)
        self.player.location.treasure = None

    def initial_room(self):
        if self.player.location.function == 'treasure':
            self.treasure()
        elif self.player.location.function == 'monster':
            self.fight()
        else:
            pass
        self.player.location.visited = True

    def move_north(self):
        if self.player.location.neighbor['N'] is not None:
            self.all_buttons = pygame.sprite.Group()
            self.all_text = pygame.sprite.Group()
            self.player.location = self.player.location.neighbor['N']
            self.initial_room()
            self.dungeon_map()

    def move_south(self):
        if self.player.location.neighbor['S'] is not None:
            self.all_buttons = pygame.sprite.Group()
            self.all_text = pygame.sprite.Group()
            self.player.location = self.player.location.neighbor['S']
            self.initial_room()
            self.dungeon_map()

    def move_west(self):
        if self.player.location.neighbor['W'] is not None:
            self.all_buttons = pygame.sprite.Group()
            self.all_text = pygame.sprite.Group()
            self.player.location = self.player.location.neighbor['W']
            self.initial_room()
            self.dungeon_map()

    def move_east(self):
        if self.player.location.neighbor['E'] is not None:
            self.all_buttons = pygame.sprite.Group()
            self.all_text = pygame.sprite.Group()
            self.player.location = self.player.location.neighbor['E']
            self.initial_room()
            self.dungeon_map()

    def dungeon(self):
        self.all_text = pygame.sprite.Group()
        self.all_buttons = pygame.sprite.Group()
        tiles = 10
        self.player.dung = Map(tiles)
        self.player.location = self.player.dung.rooms[int(tiles / 2)][int(tiles / 2)]
        self.player.location.visited = True
        self.game_window()

        self.dungeon_map()

    def eq(self):
        pass

    def logo(self):
        logo_text = Text(x=800 / 2, y=50, text='Welcome in RPG adventure.', color=(255, 255, 255), font=FONT)
        self.all_text.add(logo_text)

    def input_button(self, name):
        self.name = name

    def create_character_show(self):
        self.all_text = pygame.sprite.Group()
        self.all_buttons = pygame.sprite.Group()
        back_button = Button(50, 500, 150, 65, self.back, text='Back')
        start_button = Button(600, 500, 150, 65, self.start_game, text='Start')
        text_name = Text(x=50, y=150, text='Name: ', align='left')
        input_button = InputText(x=150, y=150, text=self.name, width=200, height=50, callback=self.input_button)
        warrior_button = Button(50, 300, 150, 65, self.warrior, text='Warrior')
        class_text = Text(x=50, y=100, text=f'Class: {self.character_class}', align='left')
        self.all_buttons.add(back_button, start_button, input_button, warrior_button)
        self.all_text.add(text_name, class_text)

    def start_game(self):
        self.create_character_show()
        if self.name == '':
            text_name = Text(x=400, y=525, text='You must write your name')
            self.all_text.add(text_name)
        elif self.character_class == '':
            text_name = Text(x=400, y=525, text='You must choose your class')
            self.all_text.add(text_name)
        elif self.character_class == 'Warrior':
            self.player = character.Warrior(self.name)
            try:
                saves = pickle.load(open("save.p", "rb"))
            except FileNotFoundError:
                saves = []
            exist = False
            for save in saves:
                if save.name == self.player.name:
                    exist = True
            if not exist:
                saves.append(self.player)
                pickle.dump(saves, open('save.p', 'wb'))
                self.menu = True
            else:
                player_exist = Text(x=400, y=525, text='This name is exist')
                self.all_text.add(player_exist)

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
            320, 200, 170, 65, self.new_game, text='New Game', text_color=(255, 255, 255))
        load_button = Button(
            320, 300, 170, 65, self.load, text='Load', text_color=(255, 255, 255))
        quit_button = Button(
            320, 400, 170, 65, self.quit_game, text='Quit', text_color=(255, 255, 255))
        self.all_buttons.add(new_game_button, load_button, quit_button)

    def main_menu(self):
        self.main_menu_show()
        while not self.menu:
            self.handle_events()
            self.run_logic()
            self.draw()

    def new_game(self):
        self.name = ''
        self.character_class = ''
        self.create_character_show()

    def start_loaded_game(self, save):
        self.player = save
        self.menu = True

    def load(self):
        self.all_text = pygame.sprite.Group()
        self.all_buttons = pygame.sprite.Group()
        back_button = Button(50, 500, 150, 65, self.back, text='Back')
        self.all_buttons.add(back_button)
        self.logo()
        text_name = Text(x=400, y=150, text='Choose your save')
        try:
            saves = pickle.load(open("save.p", "rb"))
        except FileNotFoundError:
            saves = []
            text_name = Text(x=400, y=150, text='There is no saves')
        self.all_text.add(text_name)
        counter = 1
        counter2 = 0
        for save in saves[::-1]:
            if counter > 4:
                counter2 += 1
                counter = 1
            save_button = Button(50 + 200 * counter2, 120 + 70 * counter, 150, 65,
                                 self.start_loaded_game, text=save.name, arg=save)
            self.all_buttons.add(save_button)
            counter += 1

    def quit_game(self):
        self.menu = True
        self.game = True

    def run_logic(self):
        self.all_buttons.update()
        pygame.display.update()

    def draw(self):
        background = btn.Background('images/background.jpg', [0, 0])
        self.screen.fill([255, 255, 255])
        self.screen.blit(background.image, background.rect)
        self.all_text.draw(self.screen)
        self.all_buttons.draw(self.screen)


if __name__ == '__main__':
    pygame.init()
    game = Game(resolution)
    game.main_menu()
    game.main_game()
    pygame.quit()
