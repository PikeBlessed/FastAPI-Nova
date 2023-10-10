from models.shirt import Shirt as ShirtModel
from schemas.shirt import Shirt

class ShirtService():

    def __init__(self, db) -> None:
        self.db = db

    def get_shirts(self):
        result = self.db.query(ShirtModel).all()
        return result

    def get_shirt(self, id):
        result = self.db.query(ShirtModel).filter(ShirtModel.id == id).first()
        return result
    
    def get_shirts_by_collection(self, collection):
        result = self.db.query(ShirtModel).filter(ShirtModel.collection == collection).all()
        return result
    
    def create_shirt(self, shirt: Shirt):
        new_shirt = ShirtModel(**shirt.dict())
        self.db.add(new_shirt)
        self.db.commit()
        return new_shirt.id
    
    def edit_shirt(self, id, shirt: Shirt):
        result = self.db.query(ShirtModel).filter(ShirtModel.id == id).first()
        result.name = shirt.name
        result.color = shirt.color
        result.size = shirt.size
        result.price = shirt.price
        result.collection = shirt.collection
        self.db.commit()
        return
    
    def delete_shirt(self, id):
        result = self.db.query(ShirtModel).filter(ShirtModel.id == id).first()
        self.db.delete(result)
        self.db.commit()
        return
    