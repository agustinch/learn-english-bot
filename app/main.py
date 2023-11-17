from fastapi import FastAPI
import pymongo
from pydantic import BaseModel


class Goal(BaseModel):
    name: str
    date: str


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post('/goals')
async def createSchedule(goal: Goal):
    myclient = pymongo.MongoClient("mongodb://root:example@mongodb:27017")
    db = myclient["goals"]
    col = db["goals"]
   
    col.insert_one({"date": goal.date,"name": goal.name})
    return True

@app.get("/goals")
async def allGoals():

    myclient = pymongo.MongoClient("mongodb://root:example@mongodb:27017")
    mydb = myclient["goals"]
    mycol = mydb["goals"]


    goals =  mycol.find({}, {"_id": 0})

    return list(goals)
