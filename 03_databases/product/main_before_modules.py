from typing import List

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Depends

from . import models, schemas
from .database import SessionLocal, engine

app = FastAPI(
    title="Products API",
    description="Details for Products API Endpoints",
    terms_of_service="https://www.github.com/abdksyed",
    contact={
        "Developer Name": "Syed Abdul Khader",
        "email": "abdksyed@gmail.com",
        "linkedin": "https://www.linkedin.com/in/syedabdul47/",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    # docs_url = "/documentation", # disable /docs
    # redoc_url = None
)

models.Base.metadata.create_all(engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# making connection to database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/product", status_code=status.HTTP_201_CREATED, tags=["Product"])
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


@app.get("/products", tags=["Product"])
def products(db: Session = Depends(get_db)):
    all_products = db.query(models.Product).all()
    return all_products


@app.get("/product/{id}", tags=["Product"])
def product(id, response: Response, db: Session = Depends(get_db)):
    single_product = (
        db.query(models.Product).filter(models.Product.id == id).first()
    )
    if not single_product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Product with id:{id} NOT FOUND"
    return single_product


@app.delete("/product/{id}", tags=["Product"])
def del_product(id, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(
        synchronize_session=False
    )
    db.commit()

    return f"Product with id:{id} Deleted"


@app.put("/product/{id}", tags=["Product"])
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


@app.get(
    "/product/limited/{id}",
    response_model=schemas.DisplayProduct,
    tags=["Product Limited Info"],
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
@app.get(
    "/products/limited",
    response_model=List[schemas.DisplayProduct],
    tags=["Product Limited Info"],
)
def products_limited(db: Session = Depends(get_db)):
    all_products = db.query(models.Product).all()

    return all_products


#### Creating Multiple Models and Establishing Relationship


@app.post(
    "/seller",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.DisplaySeller,
    tags=["Seller"],
)
def add_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(request.password)
    new_selller = models.Seller(
        username=request.username, email=request.email, password=hashed_password
    )
    # Insert the newly created object to database
    db.add(new_selller)
    db.commit()
    db.refresh(new_selller)
    return new_selller
