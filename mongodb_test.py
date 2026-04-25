from fastapi import FastAPI
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv
import os
import certifi

load_dotenv()

app = FastAPI()
DB_URL = os.getenv("MONGO_URL")

client = AsyncIOMotorClient(DB_URL,tlsCAFile=certifi.where())
db = client["euron"]
euron_data = db["euron_coll"]

class Euron(BaseModel):
    name:str
    phone:int
    city:str
    course:str

@app.post("/euron/insert")
async def euron_insert_data_helper(data:Euron):
    result = await euron_data.insert_one(data.model_dump())
    return str(result.inserted_id)

@app.get("/euron/getALl")
async def get_euron_data():
    items = []
    cursor = euron_data.find({},{"_id": 0})
    rows = await cursor.to_list()
    for row in rows:
        items.append(row)
    return items

