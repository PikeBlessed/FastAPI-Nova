from fastapi import APIRouter
from fastapi import status, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List

from config.database import Session
from models.shirt import Shirt as ShirtModel

from fastapi.encoders import jsonable_encoder

from middlewares.jwt_bearer import JWTBearer

from services.shirt import ShirtService

from schemas.shirt import Shirt

shirt_router = APIRouter()

@shirt_router.get('/shirts', tags=['get shirt'], response_model=List[Shirt], status_code=200)
def get_shirts() -> List[Shirt]:
    db = Session()
    result = ShirtService(db).get_shirts()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@shirt_router.get('/shirts/{id}', tags=['get shirt'], response_model=Shirt)
def get_shirt(id: int) -> Shirt:
    db = Session()
    result = ShirtService(db).get_shirt(id)
    if not result:
        raise HTTPException(status_code=404, detail="Ese ID no existe")
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@shirt_router.get('/shirts/', tags=['get shirt'], response_model=List[Shirt], status_code=200)
def get_shirts_by_collection(collection: str) -> List[Shirt]:
    db = Session()
    result = ShirtService(db).get_shirts_by_collection(collection)
    if not result:
        raise HTTPException(status_code=404, detail="La coleccion indicada no existe")
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@shirt_router.post('/shirts', tags=['post shirt'], response_model=dict, status_code=201, dependencies=[Depends(JWTBearer())])
def create_shirt(shirt: Shirt) -> dict:
    db = Session()
    ShirtService(db).create_shirt(shirt)
    return JSONResponse(content={'message': 'Se ha registrado la remera correctamente.'}, status_code=201)
 

@shirt_router.put('/shirts/{id}', tags=['put shirt'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def edit_shirt(id: int, shirt: Shirt) -> dict:
    db = Session()
    result = ShirtService(db).get_shirt(id)
    if not result:
        raise HTTPException(status_code=404, detail="Ese ID no existe")
    ShirtService(db).edit_shirt(id, shirt)
    return JSONResponse(content={'message': 'Se ha modificado con extio la prenda'}, status_code=200)
    

@shirt_router.delete('/shirts/{id}', tags=['delete shirt'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def delete_shirt(id: int) -> dict:
    db = Session()
    result = ShirtService(db).get_shirt(id)
    if not result:
        raise HTTPException(status_code=404, detail="Ese ID no existe")
    ShirtService(db).delete_shirt(id)
    return JSONResponse(content={'message': 'Se ha iliminado la prenda con extio'}, status_code=200)
