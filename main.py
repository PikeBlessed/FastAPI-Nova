from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field, validator
from typing import Any, Coroutine, List, Optional
 
from dotenv import load_dotenv
import os

from starlette.requests import Request

from jwt_manager import create_token, validate_token
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

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

admin_email = os.getenv('ADMIN_EMAIL')
admin_password = os.getenv('ADMIN_PASSWORD')

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != admin_email and data['password'] != admin_password:
            raise HTTPException(status_code=403, detail="Las credenciales son invalidas")

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
    return JSONResponse(content=clothes, status_code=200)

@app.get('/shirts/{id}', tags=['get shirt'], response_model=Shirt)
def get_shirt(id: int) -> Shirt:
    for item in clothes:
        if item['id'] == id:
            return JSONResponse(content=item)
    return JSONResponse(content=[], status_code=404)

@app.get('/shirts/', tags=['get shirt'], response_model=List[Shirt], status_code=200)
def get_shirt_by_category(collection: str) -> List[Shirt]:
    shirt_category = list(filter(lambda k: k['collection'] == collection, clothes))
    if not shirt_category:
        raise HTTPException(status_code=404, detail="Colección no encontrada")
    return shirt_category

max_id = max(shirt['id'] for shirt in clothes) if clothes else 0

@app.post('/shirts', tags=['post shirt'], response_model=dict, status_code=201, dependencies=[Depends(JWTBearer())])
def create_shirt(shirt: Shirt) -> dict:
    if shirt.id <= max_id or shirt.id > max_id + 2:
        raise HTTPException(status_code=400, detail="Invalid id")
    clothes.append(shirt.dict())
    return JSONResponse(content={'message': 'Se ha registrado la remera correctamente.'}, status_code=201)
    

@app.put('/shirts/{id}', tags=['put shirt'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def edit_shirt(id: int, shirt: Shirt) -> dict:
    for item in clothes:
        if item['id'] == id:
            item['name'] = shirt.name
            item['color'] = shirt.color
            item['size'] = shirt.size
            item['price'] = shirt.price
            item['collection'] = shirt.collection
            return JSONResponse(content={'message': 'Se ha modificado con extio la prenda'}, status_code=200)
    return JSONResponse(content={'message': 'No se encontró una prenda con el id proporcionado'}, status_code=404)

@app.delete('/shirts/{id}', tags=['delete shirt'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def delete_shirt(id: int) -> dict:
    for item in clothes:
        if item['id'] == id:
            clothes.remove(item)
            return JSONResponse(content={'message': 'La prenda se elimino con exito'}, status_code=200)
    return JSONResponse(content={'message': 'No se encontró una prenda con el id proporcionado'}, status_code=404)
