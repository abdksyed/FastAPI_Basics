from passlib.context import CryptContext
from sqlalchemy.orm import Session

from fastapi import APIRouter, Response, status
from fastapi.params import Depends

from .. import models, schemas
from ..database import get_db

router = APIRouter(tags=["Seller"], prefix="/seller")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#### Creating Multiple Models and Establishing Relationship


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.DisplaySeller,
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
