# med_backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import (
    customer_api,
    retailer_api,
    distributor_api,
    medicine_api,
    order_api,
    retailer_stock_api,
    distributor_stock_api,
)

# ✅ Initialize app
app = FastAPI(
    title="Medical Backend API",
    description="API for authentication, medicines, carts, and orders",
    version="1.0.0"
)

# ✅ Enable CORS (important for frontend or Swagger auth)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include all routers with prefixes and tags
app.include_router(customer_api.router, tags=["Customers"])
app.include_router(retailer_api.router, tags=["Retailers"])
app.include_router(distributor_api.router, tags=["Distributors"])
app.include_router(medicine_api.router, tags=["Medicines"])
app.include_router(order_api.router, tags=["Orders"])
app.include_router(retailer_stock_api.router, tags=["Retailer Stock"])
app.include_router(distributor_stock_api.router, tags=["Distributor Stock"])

# ✅ Root endpoint
@app.get("/", tags=["Root"])
def root():
    return {"message": "Medical Backend API is running 🚀"}
