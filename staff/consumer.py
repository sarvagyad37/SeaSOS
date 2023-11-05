from main import redis, random_available, count_available
import time

key = 'emergency_request'
group = 'staff_group'

try:
    redis.xgroup_create(key, group)
except:
    print('Group already exists!')

while True:
    try:
        # ? > means read from the last id
        results = redis.xreadgroup(group, key, {key: '>'}, None)
        
        if results != []:
            for result in results:
                obj = result[1][0][1]
                
                try:
                    if int(obj['staff_assigned']) != count_available():
                        staff = random_available(int(obj['staff_assigned']))
                        staff.current_status = obj['pk']
                        print(staff)
                        staff.save()
                
                except:
                        redis.xadd('request_waiting', dict(obj), '*')
            
        
    except Exception as e:
        print(str(e))
    time.sleep(1)