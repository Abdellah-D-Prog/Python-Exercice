from fastapi import APIRouter,HTTPException
from psycopg2.extras import RealDictCursor
from models.schemas import Camp,CampUpdate
from database.connection import get_db_connection
router= APIRouter()

@router.post("",tags=["/camps"],description="Create a camp with it's name,location,and the number of days it takes.")
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

@router.put("/{camp_id}",tags=["/camps"],description="Update a camp.")
def update_camp(camp_id,camp_update:CampUpdate):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    update_fields = []
    update_values = []
    
    if camp_update.name is not None:
        update_fields.append("name = %s")
        update_values.append(camp_update.name)
    
    if camp_update.location is not None:
        update_fields.append("location = %s")
        update_values.append(camp_update.location)
    
    if camp_update.duration_days is not None:
        update_fields.append("duration_days = %s")
        update_values.append(camp_update.duration_days)
    
    update_query = f"UPDATE camps SET {', '.join(update_fields)} WHERE id = %s"
    update_values.append(camp_id)
    
    cursor.execute(update_query, update_values)
    conn.commit()
    
    cursor.execute("SELECT * FROM camps WHERE id = %s", (camp_id,))
    updated_camp = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return {
        "message": f"Camp modifié avec succès",
        "camp": updated_camp
    }
    
@router.delete("/{camp_id}",tags=["/camps"],description="Delete a camp.")
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
    
@router.get("/all",tags=["/camps"],description="Get all the camps.")
def get_all_camps():
    conn=get_db_connection()
    cursor=conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("SELECT * FROM camps")
    camps= cursor.fetchall()
    return{"camps":camps}
    cursor.close()
    conn.close()

@router.get("/{camp_id}",tags=["/camps"],description="Get a specified camp with it's id.")
def get_camp_by_id(camp_id:int):
    conn=get_db_connection()
    cursor=conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT * FROM camps WHERE id= %s",
                   (camp_id,))
    camp=cursor.fetchone()
    return {"camp": camp}
    cursor.close()
    conn.close()

@router.get("/scoots/{camp_id}",tags=["/camps"],description="Get a specified camp with all the scooits in it.")
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
