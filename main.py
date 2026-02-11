from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.models import models
from src.routes import (
    user_routes,
    stock_routes,
    product_routes
)

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes.router)
app.include_router(stock_routes.router)
app.include_router(product_routes.router)
