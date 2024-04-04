import asyncio
import uvicorn
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field


import pickle as pk

# load the model in the env 
# Opening saved model
with open("./model/lin_model.pkl", "rb") as file:
    lin_model = pk.load(file)


# create app instance 
app = FastAPI()


# create a pedantic class for the request
class HouseRequest(BaseModel):
    bedroom_count: int = Field(gt=0, lt=100)
    net_sqm: float = Field(gt=0, lt=10000)
    center_distance: float = Field(gt=0, lt=10000)
    metro_distance: float = Field(gt=0, lt=10000)
    floor: int = Field(gt=0, lt=500)
    age: int = Field(gt=0, lt=500)
    
    

# class testing 
@app.get("/class")
async def get_greet():
    return {"Message": "Hello Class"}

# get the hello world 
@app.get("/", status_code=status.HTTP_200_OK)
async def get_hello():
    return {"hello": "world"}

# make the prediction class 
@app.post('/predict', status_code=status.HTTP_200_OK)
async def make_prediction(house_request: HouseRequest):
    try:
        single_row = [[house_request.bedroom_count, house_request.net_sqm, house_request.center_distance, house_request.metro_distance, house_request.floor, house_request.age]]
        new_value = lin_model.predict(single_row)
        return {"predicted Price ": new_value[0][0]}
    except:
        raise HTTPException(status_code=500, detail="Something went wrong.")