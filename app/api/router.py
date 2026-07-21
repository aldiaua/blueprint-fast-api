from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.classes import router as classes_router
from app.api.v1.cms import router as cms_router
from app.api.v1.health import router as health_router
from app.api.v1.landing import router as landing_router
from app.api.v1.page_sections import router as page_sections_router
from app.api.v1.settings import router as settings_router
from app.api.v1.students import router as students_router
from app.api.v1.teachers import router as teachers_router

router = APIRouter(prefix="/api/v1")

router.include_router(
    health_router,
    tags=["Health"],
)

router.include_router(
    auth_router,
    tags=["Auth"],
)

router.include_router(
    teachers_router,
    tags=["Teachers"],
)

router.include_router(
    classes_router,
    tags=["Classes"],
)

router.include_router(
    students_router,
    tags=["Students"],
)

router.include_router(
    settings_router,
    tags=["Settings"],
)

router.include_router(
    page_sections_router,
    tags=["PageSections"],
)

router.include_router(
    landing_router,
    tags=["Landing"],
)

router.include_router(
    auth_router,
)

router.include_router(
    cms_router,
    tags=["CMS"],
)
