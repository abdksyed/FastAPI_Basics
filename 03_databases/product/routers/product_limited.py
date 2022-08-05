from typing import List

from sqlalchemy.orm import Session

from fastapi import APIRouter, HTTPException, Response, status
from fastapi.params import Depends

from .. import models, schemas
from ..database import get_db

router = APIRouter(tags=["Product Limited Info"])


# Response Model
# In products.py examples, when getting single product or all product details
# We are sending all the columns in the response. What if we want to send selected
# Columns only in the response.
# Hence, we create a new Class in schemas which will be used as Display class.


@router.get(
    "/product/limited/{id}",
    response_model=schemas.DisplayProduct,
)
def product_limited(id, db: Session = Depends(get_db)):
    selected_product = (
        db.query(models.Product).filter(models.Product.id == id).first()
    )
    if not selected_product:
        # response.status_code = status.HTTP_404_NOT_FOUND
        ## When running above it gives Internal Server Error.
        ## pydantic.error_wrappers.ValidationError: 3 validation errors for DisplayProduct
        ## As the response_model is DisplayProduct which needs it's 3 fields to have data.
        ## So we directly raise an Exception here.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prodcut with id:{id} NOT FOUND",
        )

    return selected_product


# Since .all() returns all the Products in a list.
# We have to enclose the schemas.DisplayProduct in a List.
@router.get(
    "/products/limited",
    response_model=List[schemas.DisplayProduct],
)
def products_limited(db: Session = Depends(get_db)):
    all_products = db.query(models.Product).all()

    return all_products
