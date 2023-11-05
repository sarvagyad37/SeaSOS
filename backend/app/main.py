from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .models import get_redis
from .redis_manager import get_room_number_by_username
from typing import Optional

app = FastAPI()

class EmergencyRequest(BaseModel):
    username: str
    location: str
    issue: Optional[str] = None
    isResolved: Optional[bool] = False
    
    class Meta:
        database = get_redis()
    

@app.post("/emergency")
def emergency_help(request: EmergencyRequest):
    try:
        room_number = get_room_number_by_username(request.username)
        emergency_request = EmergencyRequest(username=request.username, location=request.location, issue=request.issue, isResolved=request.isResolved)
        emergency_request.save()
        return {"status": "success", "data": emergency_request, "room_number": room_number}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

