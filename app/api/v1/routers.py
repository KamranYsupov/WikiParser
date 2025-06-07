from fastapi import APIRouter

from .endpoints.article import router as articles_router


api_router = APIRouter()
api_router.include_router(articles_router)
