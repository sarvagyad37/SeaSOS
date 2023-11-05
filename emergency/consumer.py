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
        # ? > means read from the last id
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