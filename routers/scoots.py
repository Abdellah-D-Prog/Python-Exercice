from fastapi import APIRouter,HTTPException
from psycopg2.extras import RealDictCursor
from models.schemas import Scoot,ScootUpdate
from database.connection import get_db_connection

router= APIRouter()

@router.post("/scoots",tags=["/scoots"],description="create a scoot with their age,group and camp id if they're related to a camp.")
def create_scoot(scoot:Scoot):
    conn=get_db_connection()
    cursor=conn.cursor()
    
    camp_id_value = scoot.camp_id if scoot.camp_id and scoot.camp_id > 0 else None
    
    cursor.execute("INSERT INTO scoots(name,age,group_name,camp_id) VALUES(%s,%s,%s,%s) RETURNING id",
                   (scoot.name,scoot.age,scoot.group_name,scoot.camp_id))
    scoot_id=cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return {"message" : f"scoot crée avec l'ID {scoot_id}",
            "scoot":scoot.model_dump()
            }

@router.put("/scoot/{scoot_id}",description="Update a scoot's information")
def update_scoot(scoot_id:int,scoot_update:ScootUpdate):
    conn=get_db_connection()
    cursor=conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("SELECT * from scoots WHERE id = %s",
                   (scoot_id,))
    scoot=cursor.fetchone()

    update_fields=[]
    update_values=[]
    
    if scoot_update.name is not None:
        update_fields.append("name = %s")
        update_values.append(scoot_update.name)
    
    if scoot_update.age is not None:
        update_fields.append("age = %s")
        update_values.append(scoot_update.age)
    
    if scoot_update.group_name is not None:
        update_fields.append("group_name = %s")
        update_values.append(scoot_update.group_name)
    
    if scoot_update.camp_id is not None:
        if scoot_update.camp_id == 0:
            update_fields.append("camp_id = %s")
            update_values.append(None)
        else:
            update_fields.append("camp_id = %s")
            update_values.append(scoot_update.camp_id)
    
    update_query=f"UPDATE scoots SET {', '.join(update_fields)} WHERE id = %s"
    update_values.append(scoot_id)
    
    cursor.execute(update_query,update_values)
    conn.commit()
    
    cursor.execute("SELECT * FROM scoots WHERE id= %s",
                   (scoot_id,))
    updated_scoot = cursor.fetchone()
    
    return{
        "message": f"Scout modifié avec succès",
        "scoot":updated_scoot
    }
    
    cursor.close(
    conn.close()
    )
    
@router.delete("/{scoot_ids}",tags=["/scoots"],description="Delete a scoot.")
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

@router.get("/scoots/all",tags=["/scoots"],description="Get a list of all the scoots.")
def get_all_scoots():
    conn=get_db_connection()
    cursor=conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("SELECT * from scoots")
    scoots=cursor.fetchall()
    return {"scoots": scoots}
    cursor.close()
    conn.close()

@router.get("/scoots/{scoot_id}",tags=["/scoots"],description="Get a specified scoot with their id.")
def get_scoot_by_id(scoot_id:int):
    conn=get_db_connection()
    cursor=conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT * FROM scoots WHERE id= %s",
                   (scoot_id,))
    scoot=cursor.fetchone()
    return {"scoot": scoot}
    cursor.close()
    conn.close()

@router.get("/scoots/camp/{scoot_id}",tags=["/scoots"],description="Get the scoot's camp.")
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
