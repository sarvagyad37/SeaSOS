from .models import User
from redis_om import Migrator

Migrator().run()

def get_room_number_by_username(username: str) -> str:
    user = User.find(User.username == username).first()
    if user:
        return user.room_number
    else:
        raise ValueError("Username not found")