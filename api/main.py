import uvicorn
from fastapi import FastAPI

from db.Session import get_db
from routers.user import router as user_router

app = FastAPI(
    title="EcoBuild-AI API",
    version="0.0.1"
)

router_list = [ user_router ]

get_db()

@app.get("/")
async def root() -> dict:  # type: ignore
    """Endpoint de verificacao -- confirma que a API esta viva."""
    return {"status": "ok"} # type: ignore

for router in router_list:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
