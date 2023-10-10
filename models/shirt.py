from config.database import Base
from sqlalchemy import Column, Integer, String

class Shirt(Base):

    __tablename__ = "shirts"

    id = Column(Integer, primary_key= True, autoincrement=True)
    name = Column(String)
    color = Column(String)
    size = Column(String)
    price = Column(Integer)
    collection = Column(String)