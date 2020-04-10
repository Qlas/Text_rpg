import numpy as np
import random
import sys


class Room:
    def __init__(self, function):
        self.neighbor = {
            'N': None,
            'S': None,
            'W': None,
            'E': None,
        }
        self.function = function
        # if player visit this room, this will change to True
        self.visited = False
        self.treasure = None

    def __str__(self):
        # before the player visits this room, he will not know what is inside
        if self.visited:
            return self.function
        else:
            return '?'


class Map:
    def __init__(self, tiles):
        # map is 2 times bigger than rooms we will have
        self.rooms = np.empty((tiles, tiles), dtype=object)
        # start room is in the middle
        self.rooms[int(tiles/2)][int(tiles/2)] = Room('start')
        self.tiles = tiles
        self.seed = random.randrange(sys.maxsize)
        random.seed(self.seed)
        self.build_map()

    def build_map(self):
        try:
            self.generate()
        except IndexError:
            self.rooms = np.empty((self.tiles, self.tiles), dtype=object)
            self.rooms[int(self.tiles / 2)][int(self.tiles / 2)] = Room('start')
            self.build_map()

    def generate(self):
        # list of function with weight
        function = ['monster'] * 1 + ['treasure'] * 1 + ['nothing'] * 1
        result = []
        while len(result) < self.tiles:
            # reshape map to 1 dimension and return not None elements
            result = np.reshape(self.rooms, -1)
            result = [elem for elem in result if elem is not None]
            room = random.choice(result)
            # get directions which is not taken for this room
            allow_direction = [key for (key, value) in room.neighbor.items() if value is None]
            if len(allow_direction) > 0:
                # get coord of room on map
                room_coord = list(zip(np.where(self.rooms == room)[0], np.where(self.rooms == room)[1]))
                direction = random.choice(allow_direction)
                if len(result)+1 == self.tiles:
                    actual_function = 'end'
                else:
                    actual_function = random.choice(function)
                if direction == 'N':
                    # create new room with function
                    new_room = Room(actual_function)
                    # add room to map
                    self.rooms[room_coord[0][0]-1, room_coord[0][1]] = new_room
                    new_room.neighbor['S'] = room
                    room.neighbor['N'] = new_room

                    # check if new room have neighbor in other dimensional
                    if self.rooms[room_coord[0][0]-1, room_coord[0][1]-1] is not None:
                        new_room.neighbor['W'] = self.rooms[room_coord[0][0] - 1, room_coord[0][1] - 1]
                        self.rooms[room_coord[0][0] - 1, room_coord[0][1] - 1].neighbor['E'] = new_room

                    if self.rooms[room_coord[0][0]-1, room_coord[0][1]+1] is not None:
                        new_room.neighbor['E'] = self.rooms[room_coord[0][0] - 1, room_coord[0][1] + 1]
                        self.rooms[room_coord[0][0] - 1, room_coord[0][1] + 1].neighbor['W'] = new_room

                    if self.rooms[room_coord[0][0]-2, room_coord[0][1]] is not None:
                        new_room.neighbor['N'] = self.rooms[room_coord[0][0] - 2, room_coord[0][1]]
                        self.rooms[room_coord[0][0] - 2, room_coord[0][1]].neighbor['S'] = new_room

                elif direction == 'S':
                    new_room = Room(actual_function)
                    self.rooms[room_coord[0][0]+1, room_coord[0][1]] = new_room
                    new_room.neighbor['N'] = room
                    room.neighbor['S'] = new_room

                    if self.rooms[room_coord[0][0]+1, room_coord[0][1]-1] is not None:
                        new_room.neighbor['W'] = self.rooms[room_coord[0][0] + 1, room_coord[0][1] - 1]
                        self.rooms[room_coord[0][0] + 1, room_coord[0][1] - 1].neighbor['E'] = new_room

                    if self.rooms[room_coord[0][0]+1, room_coord[0][1]+1] is not None:
                        new_room.neighbor['E'] = self.rooms[room_coord[0][0] + 1, room_coord[0][1] + 1]
                        self.rooms[room_coord[0][0] + 1, room_coord[0][1] + 1].neighbor['W'] = new_room

                    if self.rooms[room_coord[0][0]+2, room_coord[0][1]] is not None:
                        new_room.neighbor['S'] = self.rooms[room_coord[0][0] + 2, room_coord[0][1]]
                        self.rooms[room_coord[0][0] + 2, room_coord[0][1]].neighbor['N'] = new_room

                elif direction == 'W':
                    new_room = Room(actual_function)
                    self.rooms[room_coord[0][0], room_coord[0][1]-1] = new_room
                    new_room.neighbor['E'] = room
                    room.neighbor['W'] = new_room

                    if self.rooms[room_coord[0][0]-1, room_coord[0][1]-1] is not None:
                        new_room.neighbor['N'] = self.rooms[room_coord[0][0] - 1, room_coord[0][1] - 1]
                        self.rooms[room_coord[0][0] - 1, room_coord[0][1] - 1].neighbor['S'] = new_room

                    if self.rooms[room_coord[0][0]+1, room_coord[0][1]-1] is not None:
                        new_room.neighbor['S'] = self.rooms[room_coord[0][0] + 1, room_coord[0][1] - 1]
                        self.rooms[room_coord[0][0] + 1, room_coord[0][1] - 1].neighbor['N'] = new_room

                    if self.rooms[room_coord[0][0], room_coord[0][1]-2] is not None:
                        new_room.neighbor['W'] = self.rooms[room_coord[0][0], room_coord[0][1] - 2]
                        self.rooms[room_coord[0][0], room_coord[0][1] - 2].neighbor['E'] = new_room

                elif direction == 'E':
                    new_room = Room(actual_function)
                    self.rooms[room_coord[0][0], room_coord[0][1]+1] = new_room
                    new_room.neighbor['W'] = room
                    room.neighbor['E'] = new_room

                    if self.rooms[room_coord[0][0]-1, room_coord[0][1]+1] is not None:
                        new_room.neighbor['N'] = self.rooms[room_coord[0][0] - 1, room_coord[0][1] + 1]
                        self.rooms[room_coord[0][0] - 1, room_coord[0][1] + 1].neighbor['S'] = new_room

                    if self.rooms[room_coord[0][0]+1, room_coord[0][1]+1] is not None:
                        new_room.neighbor['S'] = self.rooms[room_coord[0][0] + 1, room_coord[0][1] + 1]
                        self.rooms[room_coord[0][0] + 1, room_coord[0][1] + 1].neighbor['N'] = new_room

                    if self.rooms[room_coord[0][0], room_coord[0][1]+2] is not None:
                        new_room.neighbor['E'] = self.rooms[room_coord[0][0], room_coord[0][1] + 2]
                        self.rooms[room_coord[0][0], room_coord[0][1] + 2].neighbor['W'] = new_room

                result = np.reshape(self.rooms, -1)
                result = [elem for elem in result if elem is not None]
