from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes_admin import router as admin_router
from routes_auth import router as auth_router
from routes_orders import router as orders_router
from routes_products import router as products_router
from routes_users import router as users_router
from routes_utils import router as utils_router

# VULN: debug-mode-enabled — running with debug=True in what is meant to
# resemble a deployable app (exposes stack traces to clients on error).
app = FastAPI(title="Vulnerable Marketplace Demo", debug=True)

# VULN: permissive-cors — wildcard origin combined with allow_credentials=True.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(users_router)
app.include_router(admin_router)
app.include_router(utils_router)


@app.get("/")
def root():
    return {"status": "ok", "app": "vulnerable-marketplace-demo"}
