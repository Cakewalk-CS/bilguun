import random, time, requests
from settings import AUTHORIZATION_TOKEN
from room import Room, get_rooms
from models import PlayerBackup
import time

class Player:
    def __init__(self, starting_room, name=None, items=None, cooldown=1, coins=None, visited_path=None):
        self.current_room = starting_room
        self.name = name
        self.items = items
        self.cooldown = cooldown
        self.coins = coins
        self.visited_path = visited_path if visited_path else []
        self.save_player()

    def travel(self, direction, show_rooms = False):
        time.sleep(self.cooldown)
        if direction in self.current_room.exits:
            headers = {
                'Authorization': AUTHORIZATION_TOKEN,
                'Content-Type': 'application/json'
            }
            request_data = {"direction": direction} 
            # print(f'request_data: {request_data}')
            url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/move/'
            r = requests.post(url = url, json = request_data, headers = headers)
            res_data = r.json()
            print(f'res data \n {res_data} \n')
            room_id, title, description, exits, coordinates, items, terrain, elevation, cooldown  = (res_data[k] for k in('room_id', 'title', 
                'description', 'exits', 'coordinates', 'items', 'terrain', 'elevation', 'cooldown'))
            self.current_room = Room(room_id, title, description, exits, coordinates, items, terrain, elevation)
            self.cooldown = cooldown
            return self.current_room
        # if next_room is not None:
        #     self.current_room = next_room
        #     if (show_rooms):
        #         next_room.print_room_description(self)
        else:
            print("You cannot move in that direction.")

        # def save_player(self):
        self.update_player()
    
    def update_player(self):
        PlayerBackup.update({PlayerBackup.current_room_id:self.current_room.room_id, 
                            PlayerBackup.visited_path:self.visited_path,
                            PlayerBackup.cooldown:self.cooldown}).where(PlayerBackup.id == 1).execute()
    
    def save_player(self):
        PlayerBackup.replace(id=1, name=self.name, items=self.items, cooldown=self.cooldown, 
                            coins=self.coins, current_room_id=self.current_room.room_id, 
                            visited_path=self.visited_path).execute()
def get_player():
    player_info = PlayerBackup.select().dicts()[0]
    print(f'player info: {player_info}')
    name, items, coins, current_room_id, cooldown, visited_path = (player_info[k] for k in('name', 'items', 
        'coins', 'current_room_id', 'cooldown', 'visited_path'))
    visited = get_rooms()
    return Player(visited[current_room_id], name, items, cooldown, coins, eval(visited_path))