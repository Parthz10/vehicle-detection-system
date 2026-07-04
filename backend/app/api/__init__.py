from fastapi import APIRouter

from app.api import auth, blacklist, cameras, detections, streams

api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router)
api_router.include_router(cameras.router)
api_router.include_router(detections.router)
api_router.include_router(blacklist.router)
api_router.include_router(streams.router)
