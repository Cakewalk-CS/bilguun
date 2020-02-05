from player import Player, get_player
from room import Room, get_rooms,opposite_direction
# from world import World
import random, time, requests
from settings import AUTHORIZATION_TOKEN
# from models import Room, Player
# import random
# from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)


# Loads the map into a dictionary
# room_graph=literal_eval(open(map_file, "r").read())
# world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

def add_to_visited(room_id, visited):
    if room_id not in visited:
        visited[room_id] = {'n':'?', 's':'?', 'e': '?', 'w':'?'}
    return visited

# def non_visited_exits(room_id, player, visited):
#     choices = player.current_room.exits
#     possible_choices = []
#     for direction, new_room_id in visited[room_id]:
#         if direction in choices and new_room_id == '?':
#             possible_choices.append(direction)
#     return possible_choices

def random_walk(player, visited={}):
    queue = Queue()
    queue.enqueue(player.current_room.room_id)
    
    while queue.size() > 0:
        room_id = queue.dequeue()
        # visited = add_to_visited(room_id, visited)
        visited[room_id]=player.current_room
        if player.visited_path:
            pre_room_id = player.visited_path[-1][0]
            pre_room_dir = opposite_direction(player.visited_path[-1][1])
            setattr(visited[room_id], pre_room_dir, visited[pre_room_id])
            visited[pre_room_id].update_room()
        choices = visited[room_id].untraveled_exits()
        if choices:
            print('-----possible_directions-------')
            choice = random.choice(choices)
            print(f'coice {choice}\n')
            player.travel(choice)
            setattr(visited[room_id], choice, player.current_room)
            player.visited_path.append([room_id, choice])
        else:
            choice = pre_room_dir
            player.travel(choice)
            if player.visited_path:
                player.visited_path.pop()
            else:
                traversal_path.append(choice)
                return visited
        traversal_path.append(choice)
        visited[room_id].update_room()
        queue.enqueue(player.current_room.room_id)


def init_walk():
    url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/init/'
    headers = {'Authorization': AUTHORIZATION_TOKEN}
    res_data = requests.get(url=url, headers=headers)
    res_data = res_data.json()
    print(f'init_walk: {res_data}')
    # exit(1)
    # res_data.json()
    room_id, title, description, exits, coordinates, items, terrain, elevation = (res_data[k] for k in('room_id', 'title', 
        'description', 'exits', 'coordinates', 'items', 'terrain', 'elevation'))
    return Room(room_id, title, description, exits, coordinates, items, terrain, elevation)

starting_room = init_walk()
player = Player(starting_room)
visited = {}
random_walk(player, visited)

# visited = get_rooms()
# player = get_player()

# player = Player(world.starting_room)
# random_walk(player)
# i = 0
# while len(traversal_path) > 980:
#     traversal_path = []
#     random_walk(player)
#     i += 1
# print(i)


visited_rooms = get_rooms()
print(visited_room)
