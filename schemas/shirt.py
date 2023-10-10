from pydantic import BaseModel, Field, validator
from fastapi import HTTPException

class Shirt(BaseModel):
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
                    'name': 'nombre de la remera',
                    'color': 'color de la remera',
                    'size': 'talle de la remera',
                    'price': 30000,
                    'collection': 'coleccion a la que pertenece la remera'
                }
            ]
        }
    }
