from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field, validator
from typing import Any, Coroutine, List, Optional
 
from dotenv import load_dotenv

from jwt_manager import create_token, validate_token

from config.database import Session, engine, Base
from models.shirt import Shirt as ShirtModel

from fastapi.encoders import jsonable_encoder

from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer, admin_email, admin_password
app = FastAPI()

load_dotenv()


clothes = [
    {
        'id': 1,
        'name': 'Eternity',
        'color': 'black',
        'size': 'M',
        'price': 30000,
        'collection': 'Renacimiento'
    },
    {
        'id': 2,
        'name': 'The Creation',
        'color': 'black',
        'size': 'L',
        'price': 30000,
        'collection': 'Renacimiento'
    },
    {
        'id': 3,
        'name': 'Broken',
        'color': 'white',
        'size': 'M',
        'price': 30000,
        'collection': 'Renacimiento'
    },
    {
        'id': 4,
        'name': 'Stupid Love',
        'color': 'black',
        'size': 'M',
        'price': 30000,
        'collection': 'Renacimiento'
    },
    {
        'id': 5,
        'name': 'Trust the Process',
        'color': 'white',
        'size': 'L',
        'price': 30000,
        'collection': 'Renacimiento'
    },
    {
        "collection": "coleccion a la que pertenece la remera",
        "color": "color de la remera",
        "id": 0,
        "name": "nombre de la remera",
        "price": 30000,
        "size": "talle de la remera"
    }
]

app.add_middleware(ErrorHandler)

Base.metadata.create_all(bind=engine)

class User(BaseModel):
    email:str
    password:str


class Shirt(BaseModel):
    id: int = Field(...)
    name: str = Field(..., min_length=5, max_length=25)
    color: str = Field(...)
    size: str = Field(...)
    price: int = Field(...)
    collection: str = Field(..., min_length=3, max_length=25)

    @validator('color')
    def validate_color(cls, c):
        if c.lower() not in ['black', 'white']:
            raise HTTPException(status_code=400, detail="El color debe ser 'black' o 'white'")
        return c.lower()

    @validator('size')
    def validator_size(cls, s):
        if s.upper() not in ['S', 'M', 'L', 'XL', 'XLL']:
            raise HTTPException(status_code=400, detail='El talle que estas ingresando es incorrecto, los talles disponibles son: S, M, L, XL, XLL')
        return s.upper()
    
    @validator('price')
    def validate_price(cls, p):
        if p < 30000 or p > 40000:
            raise HTTPException(status_code=400, detail='El precio que esta ingresando es incorrecto, tiene que ser mayor a 30mil y menor a 40mil')
        return p

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': 0,
                    'name': 'nombre de la remera',
                    'color': 'color de la remera',
                    'size': 'talle de la remera',
                    'price': 30000,
                    'collection': 'coleccion a la que pertenece la remera'
                }
            ]
        }
    }

@app.get('/', tags=['home'])
def welcome():
    return HTMLResponse('<h1>Bienvenido a la pagina de Nova Essentia</h1>')

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == admin_email and user.password == admin_password:
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

@app.get('/shirts', tags=['get shirt'], response_model=List[Shirt], status_code=200)
def get_shirts() -> List[Shirt]:
    db = Session()
    result = db.query(ShirtModel).all()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@app.get('/shirts/{id}', tags=['get shirt'], response_model=Shirt)
def get_shirt(id: int) -> Shirt:
    db = Session()
    result = db.query(ShirtModel).filter(ShirtModel.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Ese ID no existe")
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@app.get('/shirts/', tags=['get shirt'], response_model=List[Shirt], status_code=200)
def get_shirts_by_collection(collection: str) -> List[Shirt]:
    db = Session()
    result = db.query(ShirtModel).filter(ShirtModel.collection == collection).all()
    if not result:
        raise HTTPException(status_code=404, detail="La coleccion indicada no existe")
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

max_id = max(shirt['id'] for shirt in clothes) if clothes else 0

@app.post('/shirts', tags=['post shirt'], response_model=dict, status_code=201, dependencies=[Depends(JWTBearer())])
def create_shirt(shirt: Shirt) -> dict:
    if shirt.id <= max_id or shirt.id > max_id + 2:
        raise HTTPException(status_code=400, detail="Invalid id")
    db = Session()
    new_shirt = ShirtModel(**shirt.dict())
    db.add(new_shirt)
    db.commit()
    return JSONResponse(content={'message': 'Se ha registrado la remera correctamente.'}, status_code=201)
 

@app.put('/shirts/{id}', tags=['put shirt'], response_model=dict, status_code=200)
def edit_shirt(id: int, shirt: Shirt) -> dict:
    db = Session()
    result = db.query(ShirtModel).filter(ShirtModel.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Ese ID no existe")
    result.name = shirt.name
    result.color = shirt.color
    result.size = shirt.size
    result.price = shirt.price
    result.collection = shirt.collection
    db.add(result)
    db.commit()
    db.refresh(result)
    return JSONResponse(content={'message': 'Se ha modificado con extio la prenda'}, status_code=200)
    

@app.delete('/shirts/{id}', tags=['delete shirt'], response_model=dict, status_code=200)
def delete_shirt(id: int) -> dict:
    db = Session()
    result = db.query(ShirtModel).filter(ShirtModel.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Ese ID no existe")
    db.delete(result)
    db.commit()
    return JSONResponse(content={'message': 'Se ha iliminado la prenda con extio'}, status_code=200)
