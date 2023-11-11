from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel, Field
from typing import Optional
import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="HOST_URL",
    port="PORT",
    password="PASSWORD",
    decode_responses=True,
)

class User(HashModel):
    username: str = Field(index=True)
    room: int
    full_name: str
    contact_number: str
    emergency_contact_number: str
    address: str
    city: str
    country: str
    insurance_provider: str

    class Meta:
        database = redis
        

@app.get('/user')
def all():
    # return User.all_pks()
    return [format(pk) for pk in User.all_pks()]


def format(pk: str):
    user = User.get(pk)

    return {
        'id': user.pk,
        'username': user.username,
        'full_name': user.full_name,
        'contact_number': user.contact_number,
        'emergency_contact_number': user.emergency_contact_number,
        'address': user.address,
        'city': user.city,
        'country': user.country,
        'insurance_provider': user.insurance_provider,
        'room': user.room
    }


@app.post('/user')
def create(user: User):
    return user.save()


@app.get('/user/{pk}')
def get(pk: str):
    return User.get(pk)


@app.put('/user/{pk}')
def update(pk: str, user: User):
    user = User.get(pk)
    user.username = user.username
    user.room = user.room
    return user.save()


@app.delete('/user/{pk}')
def delete(pk: str):
    return User.delete(pk)
