from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()

clothes = [
    {
        'id': 1,
        'name': 'Eternity',
        'color': 'black',
        'size': 'M',
        'price': 30000,
        'collection': 'Renaissance'
    },
    {
        'id': 2,
        'name': 'The Creation',
        'color': 'black',
        'size': 'L',
        'price': 30000,
        'collection': 'Renaissance'
    },
    {
        'id': 3,
        'name': 'Broken',
        'color': 'white',
        'size': 'M',
        'price': 30000,
        'collection': 'Renaissance'
    },
    {
        'id': 4,
        'name': 'Stupid Love',
        'color': 'black',
        'size': 'M',
        'price': 30000,
        'collection': 'Renaissance'
    },
    {
        'id': 5,
        'name': 'Trust the Process',
        'color': 'white',
        'size': 'L',
        'price': 30000,
        'collection': 'Renaissance'
    }
]

@app.get('/', tags=['home'])
def welcome():
    return HTMLResponse('<h1>Bienvenido a la pagina de Nova Essentia</h1>')

@app.get('/shirts', tags=['shirt'])
def get_shirts() -> list:
    return JSONResponse(content=clothes)