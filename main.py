from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.models import models
from src.routes import (
    user_routes,
    stock_routes,
    product_routes,
    client_routes,
    sale_routes,
    supplier_routes,
    purchase_routes,
    reports_stock_routes
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
app.include_router(client_routes.router)
app.include_router(sale_routes.router)
app.include_router(supplier_routes.router)
app.include_router(purchase_routes.router)
app.include_router(reports_stock_routes.router)
