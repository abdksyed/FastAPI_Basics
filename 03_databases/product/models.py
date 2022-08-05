import string

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


## Whenever any change is done to Tables(classes here), we will have to delete
## that table from the database and run the server again.
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    seller_id = Column(Integer, ForeignKey("sellers.id"))
    seller = relationship("Seller", back_populates="products")
    ## back-populates should have the name matching to the variable
    ## name in the class to which it is having relationship with.


class Seller(Base):
    __tablename__ = "sellers"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    products = relationship("Product", back_populates="seller")
