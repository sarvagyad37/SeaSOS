Here is a detailed explantion of EmergencyRequest in main.py:
## Summary
The EmergencyRequest class is a model class that represents an emergency request. It is used to create, update, retrieve, and delete emergency requests. The class is integrated with a Redis database and provides methods to interact with the database. 

## Example Usage
```
# Create a new emergency request
emergency_request = EmergencyRequest(
    user_id = "123",
    user_room = 101,
    user_insurance_provider = "ABC Insurance",
    message = "Help! I need medical assistance.",
    distance = 2.5,
    estimated_time = "10 minutes",
    status = "Pending",
    staff_assigned = 0
)
emergency_request.save()

# Update an existing emergency request
emergency_request.status = "Confirmed"
emergency_request.staff_assigned = 3
emergency_request.save()

# Retrieve all emergency requests
emergency_requests = get_emergencies()

# Retrieve a specific emergency request
emergency_request = get_emergency("123")

# Delete an emergency request
delete_emergency("123")
```
## Code Analysis

### Main functionalities
- Create a new emergency request and save it to the Redis database.
- Update the status and staff assigned of an existing emergency request.
- Retrieve all emergency requests or a specific emergency request from the database.
- Delete an emergency request from the database.
### Methods
- save(): Saves the emergency request to the Redis database.
- get(pk: str) -> EmergencyRequest: Retrieves an emergency request from the database based on its primary key.
- all_pks() -> List[str]: Retrieves all primary keys of the emergency requests in the database.
- delete(pk: str) -> bool: Deletes an emergency request from the database based on its primary key.
## Fields
- user_id: The ID of the user who made the emergency request.
- user_room: The room number of the user.
user_insurance_provider: The insurance provider of the user.
- message: The message describing the emergency.
- distance: The distance to the user's location.
- estimated_time: The estimated time of arrival for assistance.
- status: The status of the emergency request (e.g., "Pending", "Confirmed").
- staff_assigned: The ID of the staff member assigned to handle the emergency request.

# consumer.py:
## Summary
The code snippet creates a Redis consumer group and continuously reads messages from a Redis stream. If there are any messages in the stream, it retrieves the message, updates the status of the corresponding EmergencyRequest object, and saves it back to the database.

## Example Usage

```
from main import redis, EmergencyRequest
import time

key = 'request_waiting'
group = 'emergency_group'

try:
    redis.xgroup_create(key, group)
except:
    print('Group already exists!')

while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)
        print(results)
        if results != []:
            for result in results:
                obj = result[1][0][1]
                print(obj)
            
                emergency_request = EmergencyRequest.get(obj['pk'])
                emergency_request.status = 'waiting'
                print(emergency_request)
                emergency_request.save()
    
    except Exception as e:
        print(str(e))
    time.sleep(1)
```
## Code Analysis
#### Inputs
- redis: Redis connection object.
- EmergencyRequest: A class representing an emergency request.
- key: The name of the Redis stream.
- group: The name of the Redis consumer group.
#### Flow
- The code snippet attempts to create a Redis consumer group using the xgroup_create method. If the group already exists, it prints a message indicating that.
- The code enters an infinite loop.
- Inside the loop, it reads messages from the Redis stream using the xreadgroup method.
- If there are any messages in the stream, it retrieves the message and extracts the payload.
- It retrieves the corresponding EmergencyRequest object from the database using the primary key (pk) extracted from the payload.
- It updates the status of the EmergencyRequest object to 'waiting'.
- It saves the updated EmergencyRequest object back to the database.
- If any exception occurs during the process, it prints the error message.
The code then waits for 1 second before repeating the loop.
#### Outputs
- The code snippet prints the results of reading the Redis stream and the extracted payload.
- If there are any messages in the stream, it prints the updated EmergencyRequest object.
