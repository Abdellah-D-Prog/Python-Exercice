from fastapi import FastAPI
import uvicorn
#import docker 
from dotenv import load_dotenv

load_dotenv()

from routers import scoots,camps


app=FastAPI(title="Scout API",
            description="API de gestion de scouts et camps Scouts !",
            tags=[{"name": "/scoots"},{"name":"/camps"}]
            )

#Inclure les routers pour les endpoints Scoots et Camps
app.include_router(scoots.router,prefix="/scoots",tags=["/scoots"])
app.include_router(camps.router,prefix="/camps",tags=["/camps"])

if __name__ == "__main__":
    print("Démarrage de l'API Python scoot...")
    uvicorn.run(app, host="localhost", port=8000)