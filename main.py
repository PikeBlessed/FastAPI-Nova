from fastapi import FastAPI
from fastapi.responses import HTMLResponse
 
from dotenv import load_dotenv

from config.database import engine, Base

from middlewares.error_handler import ErrorHandler

from routers.shirt import shirt_router
from routers.user import user_router

app = FastAPI()

load_dotenv()

app.add_middleware(ErrorHandler)
app.include_router(user_router)
app.include_router(shirt_router)


Base.metadata.create_all(bind=engine)

@app.get('/', tags=['home'])
def welcome():
    return HTMLResponse('<h1>Bienvenido a la pagina de Nova Essentia</h1>')


