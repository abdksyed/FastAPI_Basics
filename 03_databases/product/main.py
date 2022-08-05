from fastapi import FastAPI

from . import models
from .database import engine
from .routers import product, product_limited, seller

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

app.include_router(product.router)
app.include_router(product_limited.router)
app.include_router(seller.router)


models.Base.metadata.create_all(engine)
