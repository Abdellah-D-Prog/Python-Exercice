#import des différents outils
from fastapi import FastAPI,HTTPException
import uvicorn
#import docker 
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

#pour instancier FastAPI
app=FastAPI(title="Python Scout")

load_dotenv()

#Configuration BDD
DB_CONFIG ={
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user" : os.getenv("DB_USER"),
    "password" : os.getenv("DB_PASSWORD")
}
#Instanciation des classes Scout et Camp
class Scout(BaseModel):
    name:str
    age:int
    group_name:str
    
class Camp(BaseModel):
    name:str
    location:str
    duration_days:int
    
#Permettre la connection à la BDD

def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        raise

#Les différents ENDPOINTS

#Racine
@app.get("/")
def root():
    return {"message" : "Python Scout API"}

#Scout

#Pour créer un scout
@app.post("/scoots")
def create_scout(scout:Scout):
    conn=get_db_connection()
    cursor=conn.cursor()
    cursor.execute("INSERT INTO scouts(name,age,group_name) VALUES(%s,%s,%s) RETURNING id",
                   (scout.name,scout.age,scout.group_name))
    scout_id=cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return {"message" : f"Scout crée avec l'ID {scout_id}",
            "scout":scout.dict()
            }


#Pour récupérer tous les scouts
@app.get("/scoots/all")
def get_all_scouts():
    conn=get_db_connection()
    cursor=conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("SELECT * from scouts")
    scouts=cursor.fetchall()
    return {"scouts": scouts}
    cursor.close()
    conn.close()
    
#Pour récupèrer un scout spécifique par id
@app.get("/scoots/{scout_id}")
def get_scout_by_id(scout_id:int):
    conn=get_db_connection()
    cursor=conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT * FROM scouts WHERE id= %s",
                   (scout_id,))
    scout=cursor.fetchone()
    return {"scout": scout}
    cursor.close()
    conn.close()

#Pour supprimer un scout
@app.delete("/scoots/delete/{scout_ids}")
def delete_scout(scout_id: int):
    conn=get_db_connection()
    cursor=conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("SELECT * from scouts WHERE id = %s",
                   (scout_id,))
    scout=cursor.fetchone()
    cursor.execute("DELETE FROM scouts WHERE id = %s",
                  (scout_id,))
    conn.commit()
    return{"message": f"Le scout avec l'ID {scout_id} est supprimé.",
           "scout_deleted":scout}
    cursor.close()
    conn.close()

#Camp

#Pour créer un camp
@app.post("/camps")
def create_camp(camp:Camp):
    conn=get_db_connection()
    cursor=conn.cursor()
    
    cursor.execute("INSERT INTO camps(name,location,duration_days) VALUES(%s,%s,%s) RETURNING id",
                   (camp.name,camp.location,camp.duration_days))
    camp_id=cursor.fetchone()[0]
    conn.commit()
    return{"message": f"Camp crée avec l'ID {camp_id}",
           "camp":camp.dict()}
    cursor.close()
    conn.close()
    
#Pour supprimer un camp
@app.delete("/camps/delete/{camp_id}")
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
    
#pour afficher tous les camps
@app.get("/camps/all")
def get_all_camps():
    conn=get_db_connection()
    cursor=conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("SELECT * FROM camps")
    camps= cursor.fetchall()
    return{"camps":camps}
    cursor.close()
    conn.close()
    
#Pour afficher un camp par ID
if __name__ == "__main__":
    print("Démarrage de l'API Python Scout...")
    uvicorn.run(app, host="localhost", port=8000)