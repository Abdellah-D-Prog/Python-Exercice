#import des différents outils
from fastapi import FastAPI
import uvicorn
#import docker 
from pydantic import BaseModel

app=FastAPI(title="Python Scout")


class Scout(BaseModel):
    name:str
    age:int
    group_name:str
    
class Camp(BaseModel):
    name:str
    location:str
    duration_days:int
