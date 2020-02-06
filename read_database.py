import random, time, requests
from settings import AUTHORIZATION_TOKEN
from player import Player, get_player
from room import Room, get_rooms,opposite_direction
from models import PlayerBackup, RoomBackup
from ast import literal_eval

class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}
    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()
    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        If both exist, and a connection from v1 to v2
        """
        if v1 in  self.vertices  and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError("That vertex does not exist!")


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
''' 
    {'room_id': {n: 123, s: 43}}
    {}'''
def get_connections_from_db():
    connections = {}
    items = {}
    rooms = RoomBackup.select()
    for room in rooms:
        connections[room.room_id] = literal_eval(room.connections)
        items[room.room_id] = literal_eval(room.items)
    return connections

#  def bft(self, starting_vertex):
#     queue = Queue()
#     queue.enqueue(starting_vertex)
#     visited = set()
#     visited_list = []
#     while queue.size() > 0:
#         vertex = queue.dequeue()
#         if vertex not in visited:
#     #       DO THE THING!
            
#             visited_list.append(vertex)
#             visited.add(vertex)
# #       For each edge in the item
#         for next_vert in self.get_neighbors(vertex):
# #           Add that edge to the queue/stack
#             queue.enqueue(next_vert)
#     return visited_list

def bfs(starting_vertex, destination_vertex):
    connections = get_connections_from_db()
    # starting_vertex = random.choice(list(connections))
    # starting_vertex = player.current_room.room_id
    # destination_vertex = random.choice(list(connections))
    print(starting_vertex)
    print(destination_vertex)
    print(connections)
    queue = Queue()
    queue.enqueue([["b",starting_vertex]])
    visited = set()
    while queue.size() > 0:
        path = queue.dequeue()
        vertex = path[-1][1]
        if vertex not in visited:
            if vertex == destination_vertex:
                print(path)
                return path
            visited.add(vertex)
            for direction, next_vertex in connections[vertex].items():
                # print(path)
                new_path = list(path) 
                new_path.append([direction, next_vertex])
                queue.enqueue(new_path)
    print(connections)

def init_walk():
    url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/init/'
    headers = {'Authorization': AUTHORIZATION_TOKEN}
    res_data = requests.get(url=url, headers=headers)
    res_data = res_data.json()
    print(res_data)
    room_id, title, description, exits, coordinates, items, terrain, elevation = (res_data[k] for k in('room_id', 'title', 
        'description', 'exits', 'coordinates', 'items', 'terrain', 'elevation'))
    return Room(room_id, title, description, exits, coordinates, items, terrain, elevation)

# starting_room = init_walk()
# player = get_player()
while True:
    time.sleep(15)
    print('\n\n')
    print('----------------------------------------------------')
    bfs(99, 20)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0])
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")