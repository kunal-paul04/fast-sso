from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from app.database import get_mongo_client, MONGO_DB, MONGO_COLLECTION

# REST API Router
router = APIRouter()


class ProfileRequest(BaseModel):
    email: EmailStr


@router.post("/get_profile")
async def get_info(request: ProfileRequest, mongo_client=Depends(get_mongo_client)):
    db = mongo_client[MONGO_DB]
    users_collection = db[MONGO_COLLECTION]

    user = users_collection.find_one(
        {"user_email": request.email},
        {
            "_id": 0,
            "unique_id": 1,
            "user_email": 1,
            "name": 1,
            "passkey": 1,
            "profile_pic": 1,
            "address": 1,
            "city_id": 1,
            "country_id": 1,
            "dob": 1,
            "gender": 1,
            "state_id": 1,
            "user_phone": 1,
            "zip": 1
        }
    )

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {"success": True, "data": user}
