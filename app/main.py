#-- Project start in console
#      .\venv\Scripts\activate
#      uvicorn app.main:app --reload

from fastapi import FastAPI
from app.routers import api1_broken_object_level_auth
from app.routers import api2_broken_authentication
from app.routers import api3_broken_object_property_level_auth
from app.routers import api4_unrestricted_resource_consumption
from app.routers import api5_broken_function_level_auth
from app.routers import api6_unrestricted_access_sensitive_flows
from app.routers import api7_server_side_request_forgery
from app.routers import api8_security_misconfiguration
from app.routers import api9_improper_inventory_management
from app.routers import api10_unsafe_consumption_of_apis

app = FastAPI(title="OWASP API Security Top 10 Demo")

# Inclusão das rotas
app.include_router(api1_broken_object_level_auth.router,            prefix="/api1", tags=["API1 - BOLA"])
app.include_router(api2_broken_authentication.router,               prefix="/api2", tags=["API2 - Broken Auth"])
app.include_router(api3_broken_object_property_level_auth.router,   prefix="/api3", tags=["API3 - Property Auth"])
app.include_router(api4_unrestricted_resource_consumption.router,   prefix="/api4", tags=["API4 - Resource Consumption"])
app.include_router(api5_broken_function_level_auth.router,          prefix="/api5", tags=["API5 - Function Level Auth"])
app.include_router(api6_unrestricted_access_sensitive_flows.router, prefix="/api6", tags=["API6 - Sensitive Flows"])
app.include_router(api7_server_side_request_forgery.router,         prefix="/api7", tags=["API7 - SSRF"])
app.include_router(api8_security_misconfiguration.router,           prefix="/api8", tags=["API8 - Security Misconfiguration"])
app.include_router(api9_improper_inventory_management.router,       prefix="/api9", tags=["API9 - Inventory Management"])
app.include_router(api10_unsafe_consumption_of_apis.router,         prefix="/api10", tags=["API10 - Unsafe Consumption"])