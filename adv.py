from player import Player, get_player
from room import Room, get_rooms,opposite_direction
import random, time, requests
from settings import AUTHORIZATION_TOKEN

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

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# def return_visited_path(player):
#     print(f'---Visited Path: {player.visited_path} :---')
#     if player.visited_path:
#         pre_room_id = player.visited_path[-1][0]
#         pre_room_dir = opposite_direction(player.visited_path[-1][1])
#         return pre_room_id, pre_room_dir

def random_walk(player, visited={}):
    queue = Queue()
    #adds player's current room id into the queue
    queue.enqueue(player.current_room.room_id)
    while queue.size() > 0:
        #removes current room id from the queue
        room_id = queue.dequeue()
        #if room id is 0 break out of the loop
        if room_id == 0:
            break
        # current room will become from room
        visited[room_id] = player.current_room
        #getting untraveled choices from current room
        choices = visited[room_id].untravelled_exits
        print(f'-------choices: {choices} :-----------')
        # pre_room_id, pre_room_dir = return_visited_path(player)
        if player.visited_path:
            pre_room_id = player.visited_path[-1][0]
            pre_room_dir = opposite_direction(player.visited_path[-1][1])
        if choices:
            choice = random.choice(choices)
            print(f'-------chosen one: {choice} :-----------')
            print(f'---traveling to an unknown room by going {choice}')
            player.travel(choice)
            # add to visited path if the path is
            player.visited_path.append([room_id, choice])
            # player.pickup_items()
            # player.check_items()
        else:
            choice = pre_room_dir
            room_id = pre_room_id
            print(f'-------travelling to {room_id} by going {choice} , backwards:----------')
            player.travel(choice, room_id)
            # if player.visited_path:
            popped_choice = player.visited_path.pop()
            print(f'-----popped: {popped_choice} :-------')
            # else:
            #     return visited
        queue.enqueue(player.current_room.room_id)



def init_walk():
    url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/init/'
    headers = {'Authorization': AUTHORIZATION_TOKEN}
    res_data = requests.get(url=url, headers=headers)
    res_data = res_data.json()
    print(res_data)
    room_id, title, description, exits, coordinates, items, terrain, elevation = (res_data[k] for k in('room_id', 'title', 
        'description', 'exits', 'coordinates', 'items', 'terrain', 'elevation'))
    return Room(room_id, title, description, exits, coordinates, items, terrain, elevation)


#Uncomment if starting fresh
starting_room = init_walk()
player = Player(starting_room)
visited = {}

#Uncomment when you already have info in db
# visited = get_rooms()
# player = get_player()

random_walk(player, visited)

# player = Player(world.starting_room)
# random_walk(player)
# i = 0
# while len(traversal_path) > 980:
#     traversal_path = []
#     random_walk(player)
#     i += 1
# print(i)



######
# UNCOMMENT TO WALK AROUND
######
# player.current_room.print_room_description(player)
# while True:
#     print(player.current_room)
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0])
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")