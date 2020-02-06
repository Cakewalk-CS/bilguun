from peewee import *
import datetime


db = SqliteDatabase('treasure_hunt.db')

class BaseModel(Model):
    class Meta:
        database = db

class RoomBackup(BaseModel):
    room_id = IntegerField(unique=True)
    title = TextField()
    description = TextField()
    exits = TextField()
    coordinates = TextField()
    items = TextField()
    terrain = TextField(null=True)
    elevation = IntegerField(null=True)
    connections = TextField(null=True)
    untravelled_exits = TextField(null=True)

class PlayerBackup(BaseModel):
    name = TextField(null=True)
    items = TextField(null=True)
    coins = TextField(null=True)
    current_room_id = IntegerField(default=0)
    cooldown = FloatField(default=1)
    visited_path = TextField(null=True)
    traversal_path = TextField(null=True)
    created_date = DateTimeField(default=datetime.datetime.now)

def create_tables():
    db.connect()
    db.create_tables([RoomBackup, PlayerBackup])

    
if __name__ == "__main__":
    create_tables()
