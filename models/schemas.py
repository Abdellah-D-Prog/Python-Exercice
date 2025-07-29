from pydantic import BaseModel
from typing import Optional,List

class Scoot(BaseModel):
    name:str
    age:int
    group_name:str
    camp_id: Optional[int] = None 

class ScootUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    group_name: Optional[str] = None
    camp_id: Optional[int] = None

class ScootWithCamp(BaseModel):
    id: int
    name: str
    age: int
    group_name: str
    camp_id: Optional[int] = None
    camp_name: Optional[str] = None        
    camp_location: Optional[str] = None 
    
class Camp(BaseModel):
    name:str
    location:str
    duration_days:int

class CampUpdate(BaseModel):
    name:Optional[str]=None
    location:Optional[str]=None
    duration_days:Optional[int]=None