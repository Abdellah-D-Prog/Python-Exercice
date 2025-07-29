from fastapi import FastAPI,HTTPException
import uvicorn
#import docker 
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from typing import Optional,List

app=FastAPI(title="Scout API",
            description="API de gestion de scouts et camps Scouts !",
            tags=[{"name": "/scoots"},{"name":"/camps"}]
            )

load_dotenv()


DB_CONFIG ={
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user" : os.getenv("DB_USER"),
    "password" : os.getenv("DB_PASSWORD")
}

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

class CampWithScoots(BaseModel):
    id: int
    name: str
    location: str
    duration_days: int
    scoots_count: int              
    scoots: List[dict] = []

def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        raise


@app.get("/")
def root():
    return {"message" : "scoot API"}

@app.post("/scoots",tags=["/scoots"],description="create a scoot with their age,group and camp id if they're related to a camp.")
def create_scoot(scoot:Scoot):
    conn=get_db_connection()
    cursor=conn.cursor()
    cursor.execute("INSERT INTO scoots(name,age,group_name,camp_id) VALUES(%s,%s,%s,%s) RETURNING id",
                   (scoot.name,scoot.age,scoot.group_name,scoot.camp_id))
    scoot_id=cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return {"message" : f"scoot crée avec l'ID {scoot_id}",
            "scoot":scoot.model_dump()
            }

@app.delete("/scoots/{scoot_ids}",tags=["/scoots"],description="Delete a scoot.")
def delete_scoot(scoot_id: int):
    conn=get_db_connection()
    cursor=conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("SELECT * from scoots WHERE id = %s",
                   (scoot_id,))
    scoot=cursor.fetchone()
    cursor.execute("DELETE FROM scoots WHERE id = %s",
                  (scoot_id,))
    conn.commit()
    return{"message": f"Le scoot avec l'ID {scoot_id} est supprimé.",
           "scoot_deleted":scoot}
    cursor.close()
    conn.close()

@app.get("/scoots/all",tags=["/scoots"],description="Get a list of all the scoots.")
def get_all_scoots():
    conn=get_db_connection()
    cursor=conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("SELECT * from scoots")
    scoots=cursor.fetchall()
    return {"scoots": scoots}
    cursor.close()
    conn.close()

@app.get("/scoots/{scoot_id}",tags=["/scoots"],description="Get a specified scoot with their id.")
def get_scoot_by_id(scoot_id:int):
    conn=get_db_connection()
    cursor=conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT * FROM scoots WHERE id= %s",
                   (scoot_id,))
    scoot=cursor.fetchone()
    return {"scoot": scoot}
    cursor.close()
    conn.close()

@app.get("/scoots/camp/{scoot_id}",tags=["/scoots"],description="Get the scoot's camp.")
def get_scoot_camp(scoot_id:int):
    conn=get_db_connection()
    cursor=conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("""SELECT s.id,s.name,s.age,s.group_name,s.camp_id,
                   c.name as camp_name,c.location as camp_location,c.duration_days as camp_duration_days 
                   FROM scoots s 
                   LEFT JOIN camps c 
                   ON s.camp_id = c.id 
                   WHERE s.id=%s""",
                   (scoot_id,))
    scoot=cursor.fetchone()
    return{"scoot_with_camp":scoot}
    cursor.close()
    conn.close()

#Camp

@app.post("/camps",tags=["/camps"],description="Create a camp with it's name,location,and the number of days it takes.")
def create_camp(camp:Camp):
    conn=get_db_connection()
    cursor=conn.cursor()
    
    cursor.execute("INSERT INTO camps(name,location,duration_days) VALUES(%s,%s,%s) RETURNING id",
                   (camp.name,camp.location,camp.duration_days))
    camp_id=cursor.fetchone()[0]
    conn.commit()
    return{"message": f"Camp crée avec l'ID {camp_id}",
           "camp":camp.model_dump()}
    cursor.close()
    conn.close()
    
@app.delete("/camps/{camp_id}",tags=["/camps"],description="Delete a camp.")
def delete_camp(camp_id:int):
    conn=get_db_connection()
    cursor=conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("SELECT * FROM camps WHERE id = %s",
                   (camp_id,))
    camp=cursor.fetchone()
    cursor.execute("DELETE FROM camps WHERE id = %s",
                   (camp_id,))
    conn.commit()
    return{"message": f"Le camp avec l'ID {camp_id} est supprimé.",
           "camp_deleted": camp}
    cursor.close()
    conn.close()
    
@app.get("/camps/all",tags=["/camps"],description="Get all the camps.")
def get_all_camps():
    conn=get_db_connection()
    cursor=conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("SELECT * FROM camps")
    camps= cursor.fetchall()
    return{"camps":camps}
    cursor.close()
    conn.close()

@app.get("/camps/{camp_id}",tags=["/camps"],description="Get a specified camp with it's id.")
def get_camp_by_id(camp_id:int):
    conn=get_db_connection()
    cursor=conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT * FROM camps WHERE id= %s",
                   (camp_id,))
    camp=cursor.fetchone()
    return {"camp": camp}
    cursor.close()
    conn.close()

@app.get("/camps/scoots/{camp_id}",tags=["/camps"],description="Get a specified camp with all the scooits in it.")
def get_scoots_by_camp_id(camp_id:int):
    conn=get_db_connection()
    cursor=conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("SELECT * from camps WHERE id=%s",(camp_id,))
    camp=cursor.fetchone()
    
    cursor.execute("SELECT id,name,age,group_name FROM scoots WHERE camp_id=%s ORDER BY name",(camp_id,))
    scoots=cursor.fetchall()
    return {
        "camp_id": camp_id,
        "camp_name": camp['name'],
        "scoots_count": len(scoots),
        "scoots": scoots
    }

if __name__ == "__main__":
    print("Démarrage de l'API Python scoot...")
    uvicorn.run(app, host="localhost", port=8001)