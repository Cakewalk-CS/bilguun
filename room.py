from models import RoomBackup
from peewee import IntegrityError
from ast import literal_eval
class Room:
    def __init__(self, room_id, title, description, exits, coordinates, items, terrain=None, elevation=None, untravelled_exits=None, rooms_visited=None, not_in_db=True):
        self.room_id = room_id
        self.title = title
        self.description = description
        self.exits = exits
        self.coordinates = coordinates
        self.items = items
        self.terrain = terrain
        self.elevation = elevation
        self.untravelled_exits = untravelled_exits if untravelled_exits else list(exits)
        self.rooms_visited = rooms_visited if rooms_visited else {}
        if not_in_db:
            self.save_room()

    def __str__(self):
        return (f'room_id: {self.room_id}, title: {self.title}, coordinates:{self.coordinates}, exits: {self.exits}'
                f'items: {self.items}, terrain: {self.terrain}, elevation: {self.elevation}, untravelled_exits: {self.untravelled_exits}, rooms_visited: {self.rooms_visited}')
    
    def travelled(self, exit_dir, room_id, check_exits=False):
        if check_exits and exit_dir in self.rooms_visited:
            if len(self.rooms_visited) is not len(self.exits):
                print(self.rooms_visited)
                print(self.exits)
                print(len(self.rooms_visited))
                print(len(self.exits))
                print(f'Major error')
                print(f'We have gone back when there was potential')
                print(f'This is somehting we should never do!!!')
                print(f'{self}')
                exit()
        if  exit_dir in self.exits:
            if exit_dir in self.untravelled_exits:
                print(f'-------exit_dir : {exit_dir} : ------')
                self.untravelled_exits.remove(exit_dir)
            else:
                print(f'----Traveled to somewhere we\'ve been before------')
                print(f'----{self.untravelled_exits}----')
                print(f'----direction traveling {exit_dir} ----')
            self.rooms_visited[exit_dir] = room_id
            self.update_room()
        else:
            print("The END has come!!!")
            exit(1)

    def save_room(self):
        try:
            RoomBackup.create(room_id = self.room_id, title = self.title, description = self.description,
                            exits = self.exits, coordinates = self.coordinates, items = self.items,
                            terrain = self.terrain, elevation = self.elevation, untravelled_exits = self.untravelled_exits)
        except IntegrityError:
            print('---INTEGRITYERROR ROOM ALREADY CREATED_____')
            pass
            # RoomBackup.update(room_id = self.room_id, title = self.title, description = self.description,
            #     exits = self.exits, coordinates = self.coordinates, items = self.items,
            #     terrain = self.terrain, elevation = self.elevation)
    def update_room(self):
        RoomBackup.update({RoomBackup.connections: self.rooms_visited, RoomBackup.items: self.items, RoomBackup.exits: self.exits,
                            RoomBackup.untravelled_exits: self.untravelled_exits}).where(RoomBackup.room_id == self.room_id).execute()

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
                                         literal_eval(room_info.exits), room_info.coordinates, room_info.items, 
                                          room_info.terrain, room_info.elevation,
                                          literal_eval(room_info.untravelled_exits), literal_eval(room_info.connections), False)
        for direction, room_id in literal_eval(room_info.connections).items():
            if room_id in visited:
                setattr(visited[room_info.room_id], direction, visited[room_id])
            elif room_id == old_room_id:
                setattr(visited[old_room_id], opposite_direction(direction), visited[room_id])
        old_room_id = room_info.room_id

    return visited
