from fastapi import FastAPI
from fastapi.background import BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests, random, time


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="HOST_URL",
    port="PASSWORD",
    password="PASSWORD",
    decode_responses=True,
)
        
class EmergencyRequest(HashModel):
    user_id: str
    user_room: int
    user_insurance_provider: str
    message: str
    distance: float
    estimated_time: str
    status: str
    staff_assigned: int
    
    class Meta:
        database = redis
    

@app.post('/emergency')
async def create(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    
    req = requests.get('http://localhost:8000/user/' + body['id'])
    user = req.json()
    
    emergency_request = EmergencyRequest(
        user_id = body['id'],
        user_full_name = user['full_name'],
        user_contact_number = user['contact_number'],
        user_emergency_contact_number = user['emergency_contact_number'],
        user_room = user['room'],
        user_insurance_provider = user['insurance_provider'],
        message = body['message'],
        distance = body['distance'],
        estimated_time = body['estimated_time'],
        status = "Pending",
        staff_assigned = 0,
    )
    emergency_request.save()
    
    background_tasks.add_task(update_emergency_status, emergency_request)
    
    return emergency_request
    

def update_emergency_status(emergency_request: EmergencyRequest):
    time.sleep(2)
    emergency_request.status = "Confirmed"
    # randomly select avaible staff to assign 
    emergency_request.staff_assigned = random.randint(1, 5)
    emergency_request.save()
    
    # create a set with the key emergency_request
    # redis.delete('emergency_request')
    redis.xadd('emergency_request', dict(emergency_request), '*')
    


def format(pk: str):
    emergency_request = EmergencyRequest.get(pk)

    return {
        'id': emergency_request.pk,
        'user_id': emergency_request.user_id,
        'user_full_name': emergency_request.user_full_name,
        'user_contact_number': emergency_request.user_contact_number,
        'user_emergency_contact_number': emergency_request.user_emergency_contact_number,
        'user_room': emergency_request.user_room,
        'user_insurance_provider': emergency_request.user_insurance_provider,
        'message': emergency_request.message,
        'distance': emergency_request.distance,
        'estimated_time': emergency_request.estimated_time,
        'status': emergency_request.status,
        'staff_assigned': emergency_request.staff_assigned,
        'created_at': emergency_request.created_at,
        'updated_at': emergency_request.updated_at
    }

@app.get('/emergency')
def get_emergencies():
    # return EmergencyRequest.all_pks()
    return [format(pk) for pk in EmergencyRequest.all_pks()]

@app.get('/emergency/{pk}')
def get_emergency(pk: str):
    return EmergencyRequest.get(pk)
    
@app.put('/emergency/{pk}')
def update_emergency(pk: str, emergency: EmergencyRequest):
    emergency = EmergencyRequest.get(pk)
    emergency.is_resolved = "true"
    return emergency.save()

@app.delete('/emergency/{pk}')
def delete_emergency(pk: str):
    return EmergencyRequest.delete(pk)
