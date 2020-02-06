import random, time, requests
from ast import literal_eval
from settings import AUTHORIZATION_TOKEN
from room import Room, get_rooms, opposite_direction
from models import PlayerBackup

import time

class Player:
    def __init__(self, starting_room, name=None, items=None, cooldown=1, coins=None, visited_path=None, traversal_path=None):
        self.current_room = starting_room
        self.name = name
        self.items = items
        self.cooldown = cooldown
        self.coins = coins
        self.visited_path = visited_path if visited_path else []
        self.traversal_path = traversal_path if traversal_path else []
        self.save_player()

    def travel(self, direction, wise_room_id = None):
        time.sleep(self.cooldown)
        print(f'----travel info {self.current_room.room_id, self.current_room.exits}---')
        #what is this?
        from_room_id = self.current_room.room_id
        #each step will be saved in to traversal_path list
        self.traversal_path.append((self.current_room.room_id, direction))
        #if directions exist in the response
        if direction in self.current_room.exits:
            headers = {
            'Authorization': AUTHORIZATION_TOKEN,
            'Content-Type': 'application/json'
            }
            if wise_room_id != None:
                print('---We are the wise, Beware!!-----')
                request_data = {"direction": direction, "next_room_id": f'{wise_room_id}'}
            else:
                request_data = {"direction": direction}
            url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/move/'
            r = requests.post(url = url, json = request_data, headers = headers)
            res_data = r.json()
            print(res_data)
            room_id, title, description, exits, coordinates, items, terrain, elevation, cooldown  = (res_data[k] for k in('room_id', 'title', 
                'description', 'exits', 'coordinates', 'items', 'terrain', 'elevation', 'cooldown'))
            #marking direction travelled, room id is travelling to
            self.current_room.travelled(direction, room_id, True)
            #current room becomes the room from the response
            self.current_room = Room(room_id, title, description, exits, coordinates, items, terrain, elevation)
            # print(self.current_room)
            #marking direction travelled from
            self.current_room.travelled(opposite_direction(direction), from_room_id)
            self.cooldown = cooldown
        else:
            print('majoy error')
            print(self.current_room)
            print("You cannot move in that direction.")
            exit(1)

        self.update_player()
        return self.current_room
    
    def update_player(self):
        PlayerBackup.update({PlayerBackup.current_room_id:self.current_room.room_id, 
                            PlayerBackup.visited_path:self.visited_path,
                            PlayerBackup.cooldown:self.cooldown,
                            PlayerBackup.traversal_path:self.traversal_path}).where(PlayerBackup.id == 1).execute()
    
    def save_player(self):
        PlayerBackup.replace(id=1, name=self.name, items=self.items, cooldown=self.cooldown, 
                            coins=self.coins, current_room_id=self.current_room.room_id, 
                            visited_path=self.visited_path, traversal_path=self.traversal_path).execute()

    # def pickup_items(self):
    #     if self.current_room.items:
    #         for item in self.current_room.items:
    #             headers = {
    #                 'Authorization': AUTHORIZATION_TOKEN,
    #                 'Content-Type': 'application/json'
    #             }
    #             url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/take/'
    #             r = requests.post(url = url, json = item, headers = headers)

    # def check_items(self):
    #     headers = {
    #                 'Authorization': AUTHORIZATION_TOKEN,
    #                 'Content-Type': 'application/json'
    #     }
    #     url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/status/'
    #     r = requests.post(url = url, headers = headers)
    #     print(r.json())

def get_player():
    player_info = PlayerBackup.select().dicts()[0]
    name, items, coins, current_room_id, cooldown, visited_path, traversal_path= (player_info[k] for k in('name', 'items', 
        'coins', 'current_room_id', 'cooldown', 'visited_path', 'traversal_path'))
    visited = get_rooms()
    return Player(visited[current_room_id], name, items, cooldown, coins, literal_eval(visited_path), literal_eval(traversal_path))