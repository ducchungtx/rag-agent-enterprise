from fastapi import APIRouter

from app.api import apikeys, auth, kb, rag, tenants

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(tenants.router)
api_router.include_router(kb.router)
api_router.include_router(rag.router)
api_router.include_router(apikeys.router)
