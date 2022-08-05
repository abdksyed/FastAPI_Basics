from typing import List

from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(engine)


# making connection to database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/product")
def add(request: schemas.Product, db: Session = Depends(get_db)):
    # Create new object of one of model Class.
    new_product = models.Product(
        name=request.name, description=request.description, price=request.price
    )
    # Insert the newly created object to database
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request


@app.get("/products")
def products(db: Session = Depends(get_db)):
    all_products = db.query(models.Product).all()

    return all_products


@app.get("/product/{id}")
def product(id, db: Session = Depends(get_db)):
    single_product = db.query(models.Product).filter(models.Product.id == id).first()

    return single_product


@app.delete("/product/{id}")
def del_product(id, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(
        synchronize_session=False
    )
    db.commit()

    return f"Product with id:{id} Deleted"


@app.put("/product/{id}")
def update_product(id, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        return f"Product with id:{id} NOT FOUND"
    product.update(request.dict())
    db.commit()

    return f"Product with id:{id} Succesfully Updated"


# Response Model
# Currently in above examples, when getting single product or all product details
# We are sending all the columns in the response. What if we want to send selected
# Columns only in the response.
# Hence, we create a new Class in schemas which will be used as Display class.


@app.get("/product/limited/{id}", response_model=schemas.DisplayProduct)
def product_limited(id, db: Session = Depends(get_db)):
    selected_product = db.query(models.Product).filter(models.Product.id == id).first()

    return selected_product


# Since .all() returns all the Products in a list.
# We have to enclose the schemas.DisplayProduct in a List.
@app.get("/products/limited", response_model=List[schemas.DisplayProduct])
def products_limited(db: Session = Depends(get_db)):
    all_products = db.query(models.Product).all()

    return all_products
