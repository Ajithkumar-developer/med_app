# med_backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.customer import (
    customer_api,
    medicine_api,
    order_api,
)
from .api.retailer import (
    retailer_api,
    retailer_medicine_api,
    retailer_order_api,
    retailer_report_api,
    retailer_invoice_api,
)
from .api.distributor import (
    distributor_api,
    distributor_stock_api,
    distributor_order_api,
    distributor_report_api,
    distributor_invoice_api,
)

# ✅ Initialize app
app = FastAPI(
    title="Medical Backend API",
    description="API for authentication, medicines, carts, and orders",
    version="1.0.0"
)

# ✅ Enable CORS (important for frontend or Swagger auth)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # you can restrict this later
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# ✅ Correct CORS setup
frontend_origins = [
    "https://medical-nu-olive.vercel.app",  # Production frontend
    "http://localhost:5173"                  # Local dev frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,  # explicit origin(s)
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
app.include_router(retailer_medicine_api.router, tags=["Retailer Products"])
app.include_router(retailer_order_api.router, tags=["Retailer Orders"])
app.include_router(retailer_report_api.router, tags=["Retailer Dashboard & Reports"])
app.include_router(retailer_invoice_api.router, tags=["Retailer Invoices"])
app.include_router(distributor_stock_api.router, tags=["Distributor Stock"])
# app.include_router(distributor_order_api.router, tags=["Distributor Orders"])
app.include_router(distributor_report_api.router, tags=["Distributor Dashboard & Reports"])
app.include_router(distributor_invoice_api.router, tags=["Distributor Invoices"])

# ✅ Root endpoint
@app.get("/", tags=["Root"])
def root():
    return {"message": "Medical Backend API is running 🚀"}
