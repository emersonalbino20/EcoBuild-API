import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import settings
from api.routers.analysis import router as analysis_router
from api.routers.material import router as material_router
from api.routers.organization import router as organization_router
from api.routers.plan import router as plan_router

app = FastAPI(
    title="EcoBuild-AI API",
    version="0.0.1",
)

router_list = [
    organization_router,
    plan_router,
    analysis_router,
    material_router,
]

cors_origins = [origin.strip() for origin in settings.CORS_ALLOWED_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if cors_origins != ["*"] else ["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict:
    """Endpoint de verificacao -- confirma que a API esta viva."""
    return {"status": "ok"}


@app.get("/health")
async def health() -> dict:
    return {"status": "healthy"}


for router in router_list:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=settings.PORT, reload=False)
