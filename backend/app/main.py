from fastapi import FastAPI

from app.api.v1.router import api_router
from app.db.session import check_db_connection


app = FastAPI()
app.include_router(api_router)


@app.get("/")
def health_check() -> dict[str, object]:
    db_connected = False

    try:
        db_connected = check_db_connection()
    except Exception:
        db_connected = False

    return {"status": "ok", "database_connected": db_connected}
