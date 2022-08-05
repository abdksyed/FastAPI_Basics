from sqlalchemy.orm import Session

from fastapi import APIRouter, Response, status
from fastapi.params import Depends

from .. import models, schemas
from ..database import get_db

router = APIRouter(tags=["Products"])


@router.post("/product", status_code=status.HTTP_201_CREATED)
# Can also use status_code = 201
def add_product(request: schemas.Product, db: Session = Depends(get_db)):
    # Create new object of one of model Class.
    new_product = models.Product(
        name=request.name,
        description=request.description,
        price=request.price,
        seller_id=request.seller_id,
    )
    # Insert the newly created object to database
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request


@router.get("/products")
def products(db: Session = Depends(get_db)):
    all_products = db.query(models.Product).all()
    return all_products


@router.get("/product/{id}")
def product(id, response: Response, db: Session = Depends(get_db)):
    single_product = (
        db.query(models.Product).filter(models.Product.id == id).first()
    )
    if not single_product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Product with id:{id} NOT FOUND"
    return single_product


@router.delete("/product/{id}")
def del_product(id, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(
        synchronize_session=False
    )
    db.commit()

    return f"Product with id:{id} Deleted"


@router.put("/product/{id}")
def update_product(id, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        return f"Product with id:{id} NOT FOUND"
    product.update(request.dict())
    db.commit()

    return f"Product with id:{id} Succesfully Updated"
