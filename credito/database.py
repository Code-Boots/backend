from bson import ObjectId
import motor.motor_asyncio
from .env import ENV

client = motor.motor_asyncio.AsyncIOMotorClient(ENV.MONGODB_URL)
db: motor.motor_asyncio.AsyncIOMotorDatabase = client["credito"]


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
