from pydantic import BaseModel


class Product(BaseModel):
    name: str
    description: str
    price: float
    seller_id: int


class Seller(BaseModel):
    username: str
    email: str
    password: str


class DisplaySeller(BaseModel):
    username: str
    email: str
    # Not displaying the password

    class Config:
        orm_mode = True


class DisplayProduct(BaseModel):

    id: int
    name: str
    description: str
    seller: DisplaySeller
    # Not displaying the price of the product

    class Config:
        orm_mode = True


## DisplayProduct output.
# {
#     "id": 1,
#     "name": "Google Pixel 6",
#     "description": "Google Pixel 6 Kinda Coral",
#     "seller": {
#         "username": "GoogleUS",
#         "email": "newyorkStore@google.com"
#     }
# }
