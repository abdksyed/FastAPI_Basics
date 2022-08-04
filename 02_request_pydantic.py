from typing import List, Set

from pydantic import BaseModel, Field, HttpUrl

from fastapi import FastAPI, Form


class Profile(BaseModel):
    name: str
    email: str
    age: int


class User(BaseModel):
    username: str = Form(...)
    password: str = Form(...)
    # profile: Profile


class Image(BaseModel):
    name: HttpUrl
    url: str


class Product(BaseModel):
    name: str
    price: float = Field(
        title="Price of Product", description="The Marked Price of the Product"
    )
    discount: int
    discounted_price: float = Field(description="Auto Calculated, if discount is given")
    tags: Set[str] = Field(
        example=["Electronics", "Phone"]
    )  # Gets overwritten with Config Example
    images: List[Image]

    class Config:
        schema_extra = {
            "example": {
                "name": "iPad",
                "price": 699,
                "discount": 15,
                "discounted_price": 0,
                "tags": ["Electronics", "Computers", "Apple"],
                "images": [
                    {
                        "url": "https://www.trustedreviews.com/wp-content/uploads/sites/54/2021/09/New-ipad-9.png",
                        "name": "iPad Image",
                    },
                    {
                        "url": "https://www.trustedreviews.com/wp-content/uploads/sites/54/2021/06/iPad-Pro-12.9-2021-2-scaled.jpeg",
                        "name": "iPad Pro",
                    },
                ],
            }
        }


app = FastAPI()


@app.post("/adduser")
def adduser(profile: Profile):
    return profile


# Passing path and query parameters to Request
@app.post("/addproduct/{prod_id}")
def addproduct(
    product: Product,
    prod_id: int,  # Path Parameter
    category: str,  # Query Parameter
):
    discount_amt = (product.price * product.discount) / 100
    product.discounted_price = product.price - discount_amt

    return {"Product Id": prod_id, "Category": category, "Product": product}


@app.post("/login")
def login(user: User):
    return user
