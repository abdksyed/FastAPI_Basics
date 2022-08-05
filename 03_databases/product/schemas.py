from pydantic import BaseModel


class Product(BaseModel):
    name: str
    description: str
    price: float


class DisplayProduct(BaseModel):

    id: int
    name: str
    description: str
    # Not displaying the price of the product

    class Config:
        orm_mode = True
