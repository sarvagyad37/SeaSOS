from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel, Field
import datetime
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-12537.c256.us-east-1-2.ec2.cloud.redislabs.com",
    port=12537,
    password="bkKUvqNbSphLmUS0g28wCWW0FZQ0QfE4",
    decode_responses=True,
)

class Staff(HashModel):
    username: str = Field(index=True)
    full_name: str
    contact_number: str
    occupation: str
    domain: str
    current_location: str
    current_status: str

    class Meta:
        database = redis
        

@app.get('/staff')
def all():
    # return Staff.all_pks()
    return [format(pk) for pk in Staff.all_pks()]

# total staff count
@app.get('/staff/count')
def count():
    count = 0
    for pk in Staff.all_pks():
        count += 1
    return count

# total staff status = available
@app.get('/staff/count/available')
def count_available():
    count = 0
    for pk in Staff.all_pks():
        if Staff.get(pk).current_status == 'available':
            count += 1
    return count

# total staff count by domain (doctor, nurse, etc)
@app.post('/staff/count/domain')
def count_by_occupation(domain: str):
    count = 0
    for pk in Staff.all_pks():
        if Staff.get(pk).domain == domain:
            count += 1
    return count

# total staff count by domain (doctor, nurse, etc) and status available
@app.post('/staff/count/domain/available')
def count_by_occupation_available(domain: str):
    count = 0
    for pk in Staff.all_pks():
        if Staff.get(pk).domain == domain and Staff.get(pk).current_status == 'available':
            count += 1
    return count

def format(pk: str):
    staff = Staff.get(pk)

    return {
        'id': staff.pk,
        'username': staff.username,
        'full_name': staff.full_name,
        'contact_number': staff.contact_number,
        'occupation': staff.occupation,
        'domain': staff.domain,
        'current_location': staff.current_location,
        'current_status': staff.current_status,
    }


@app.post('/staff')
def create(staff: Staff):
    return staff.save()


@app.get('/staff/{pk}')
def get(pk: str):
    staff = Staff.get(pk)
    redis.xadd('request_waiting', dict(staff), '*')
    return staff


@app.put('/staff/{pk}')
def update(pk: str, staff: Staff):
    staff = Staff.get(pk)
    staff.username = staff.username
    staff.full_name = staff.full_name
    staff.contact_number = staff.contact_number
    staff.occupation = staff.occupation
    staff.domain = staff.domain
    staff.current_location = staff.current_location
    staff.current_status = staff.current_status
    staff.updated_at = datetime.datetime.now()
    staff.created_at = datetime.datetime.now()
    return staff.save()

def random_available( value: int):
    staff_count = Staff.count()
    
    if staff_count < value:
            for pk in Staff.all_pks():
                if Staff.get(pk).current_status == 'available':
                    return Staff.get(pk)
    elif staff_count >= value:
        count = 0
        for pk in Staff.all_pks():
            if Staff.get(pk).current_status == 'available':
                count += 1
            if count == value:
                return Staff.get(pk)
    else:
        return "No available staff"




@app.delete('/staff/{pk}')
def delete(pk: str):
    return Staff.delete(pk)
