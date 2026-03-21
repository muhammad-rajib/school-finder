from fastapi import APIRouter

from app.api.v1.endpoints import notice, result, school, school_image, teacher


api_router = APIRouter(prefix="/api/v1")
api_router.include_router(notice.router, tags=["notices"])
api_router.include_router(result.router, tags=["results"])
api_router.include_router(school.router, tags=["schools"])
api_router.include_router(school_image.router, tags=["school-images"])
api_router.include_router(teacher.router, tags=["teachers"])
