from fastapi import APIRouter,HTTPException
from psycopg2.extras import RealDictCursor
from models.schemas import Scoot,ScootUpdate
from database.connection import get_db_connection

router= APIRouter()

@router.post("/",tags=["/scoots"],description="create a scoot with their age,group and camp id if they're related to a camp.")
def create_scoot(scoot:Scoot):   
    if scoot.age < 5:
        raise HTTPException(status_code=400, detail="L'âge ne peut pas être inférieur à 5 ans")
    if scoot.age > 17:
        raise HTTPException(status_code=400, detail="L'âge ne peut pas dépasser 17 ans")
    conn=None
    cursor=None
    
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        camp_id_value = scoot.camp_id if scoot.camp_id and scoot.camp_id > 0 else None
        
        cursor.execute("INSERT INTO scoots(name,age,group_name,camp_id) VALUES(%s,%s,%s,%s) RETURNING id",
                    (scoot.name,scoot.age,scoot.group_name,camp_id_value))
        scoot_id=cursor.fetchone()[0]
        conn.commit()
        return {"message" : f"scoot crée avec l'ID {scoot_id}",
                "scoot":scoot.model_dump()
                }
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500,detail=f"Erreur: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@router.put("/{scoot_id}",tags=["/scoots"],description="Update a scoot's information")
def update_scoot(scoot_id:int,scoot_update:ScootUpdate): 
    if scoot_update.age is not None:
        if scoot_update.age < 5:
            raise HTTPException(status_code=400, detail="L'âge ne peut pas être inférieur à 5 ans")
        if scoot_update.age > 17:
            raise HTTPException(status_code=400, detail="L'âge ne peut pas dépasser 17 ans")
    conn=None
    cursor=None
    try:
        conn=get_db_connection()
        cursor=conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("SELECT * from scoots WHERE id = %s",
                    (scoot_id,))
        scoot=cursor.fetchone()
        
        if not scoot:
            raise HTTPException(status_code=404, detail=f"Scout avec l'ID {scoot_id} non trouvé")
        
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
        
        if not update_fields:
            raise HTTPException(status_code=400,detail="Aucune donnée à mettre à jour.")
        
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
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500,detail=f"Erreur: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
@router.delete("/{scoot_id}",tags=["/scoots"],description="Delete a scoot.")
def delete_scoot(scoot_id: int):
    conn=None
    cursor=None
    
    try:
        conn=get_db_connection()
        cursor=conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("SELECT * from scoots WHERE id = %s",
                    (scoot_id,))
        scoot=cursor.fetchone()
        
        if not scoot:
            raise HTTPException(status_code=404,detail=f"Scout avec l'ID {scoot_id} non trouvé.")
        
        cursor.execute("DELETE FROM scoots WHERE id = %s",
                    (scoot_id,))
        conn.commit()
        return{"message": f"Le scoot avec l'ID {scoot_id} est supprimé.",
            "scoot_deleted":scoot}
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500,detail=f"Erreur: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@router.get("/",tags=["/scoots"],description="Get a list of all the scoots.")
def get_all_scoots():
    conn=None
    cursor=None
    try:
        conn=get_db_connection()
        cursor=conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * from scoots")
        scoots=cursor.fetchall()
        return {"scoots": scoots}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Erreur: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@router.get("/{scoot_id}",tags=["/scoots"],description="Get a specified scoot with their id.")
def get_scoot_by_id(scoot_id:int):
    conn=None
    cursor=None
    try:
        conn=get_db_connection()
        cursor=conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM scoots WHERE id= %s",
                    (scoot_id,))
        scoot=cursor.fetchone()
        return {"scoot": scoot}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Erreur: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@router.get("/camp/{scoot_id}",tags=["/scoots"],description="Get the scoot's camp.")
def get_scoot_camp(scoot_id:int):
    conn=None
    cursor=None
    try:
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
        
        if not scoot:
            raise HTTPException(status_code=404,detail=f"Scout avec l'ID {scoot_id} non trouvré.")
        
        return{"scoot_with_camp":scoot}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Erreur : {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        
