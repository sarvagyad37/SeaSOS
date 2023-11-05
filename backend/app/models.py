from redis_om import HashModel, get_redis_connection, Field

# This function is for getting a connection to Redis
def get_redis():
    redis = get_redis_connection(
    host="redis-12537.c256.us-east-1-2.ec2.cloud.redislabs.com",
    port=12537,
    password="bkKUvqNbSphLmUS0g28wCWW0FZQ0QfE4",
    decode_responses=True,
    )
    return redis

# This is a model representing a User in Redis
class User(HashModel):
    username: str  = Field(index=True)
    room_number: str

    class Meta:
        database = get_redis()

# test = User(username="guest2", room_number="413")
# test.save()