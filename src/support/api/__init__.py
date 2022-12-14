from fastapi import APIRouter

from support.api.auth import router as auth_router
from support.api.tickets import router as tickets_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(tickets_router)
