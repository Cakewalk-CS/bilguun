from models import RoomBackup
from peewee import IntegrityError
class Room:
    def __init__(self, room_id, title, description, exits, coordinates, items, terrain=None, elevation=None):
        self.room_id = room_id
        self.title = title
        self.description = description
        self.exits = exits
        self.coordinates = coordinates
        self.items = items
        self.terrain = terrain
        self.elevation = elevation
        self.n = None
        self.s = None
        self.e = None
        self.w = None
        self.save_room()

    def untraveled_exits(self):
        manual_exits = []
        if self.n is None:
            manual_exits.append("n")
        if self.s is None:
            manual_exits.append("s")
        if self.w is None:
            manual_exits.append("w")
        if self.e is None:
            manual_exits.append("e")
        yay_exits = []
        for direction in self.exits:
            if direction in manual_exits:
                print(f'unvisited directions: {direction}')
                yay_exits.append(direction)
            # if getattr(self, direction, None) is None:
        return yay_exits

    def save_room(self):
        try:
            RoomBackup.create(room_id = self.room_id, title = self.title, description = self.description,
                            exits = self.exits, coordinates = self.coordinates, items = self.items,
                            terrain = self.terrain, elevation = self.elevation)
        except IntegrityError:
            pass
            # RoomBackup.update(room_id = self.room_id, title = self.title, description = self.description,
            #     exits = self.exits, coordinates = self.coordinates, items = self.items,
            #     terrain = self.terrain, elevation = self.elevation)
    def update_room(self):
        rooms_visited = []
        for direction in self.exits:
            possible_room = getattr(self, direction, None)
            if possible_room is not None:
                rooms_visited.append((direction, possible_room.room_id))
        print(f'update_room: room id: {self.room_id}, room visited: {rooms_visited}\n')
        RoomBackup.update({RoomBackup.connections: rooms_visited}).where(RoomBackup.room_id == self.room_id).execute()

def opposite_direction(direction):
    if direction == 'n':
        return 's'
    if direction == 's':
        return 'n'
    if direction == 'e':
        return 'w'
    if direction == 'w':
        return 'e'
        
def get_rooms():
    visited = {}
    old_room_id = ''
    for room_info in RoomBackup.select():
        visited[room_info.room_id] = Room(room_info.room_id, room_info.title, room_info.description, 
                                          room_info.exits, room_info.coordinates, room_info.items, 
                                          room_info.terrain, room_info.elevation)
        for dirroom_id in eval(room_info.connections):
            # print(f'dirroom_id: {dirroom_id}')
            direction = dirroom_id[0]
            room_id = dirroom_id[1]
            if room_id in visited:
                setattr(visited[room_info.room_id], direction, visited[room_id])
            elif room_id == old_room_id:
                setattr(visited[old_room_id], opposite_direction(direction), visited[room_id])
        old_room_id = room_info.room_id
    print(f'visited rooms: {len(visited)}')
    return visited


