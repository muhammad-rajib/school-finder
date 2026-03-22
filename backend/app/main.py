from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.db.session import check_db_connection
from app.utils.responses import error_response, success_response


app = FastAPI()
app.include_router(api_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    detail = exc.detail
    message = detail if isinstance(detail, str) else "Request failed"
    data = None if isinstance(detail, str) else detail

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(message=message, data=data),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response(
            message="Validation error",
            data=exc.errors(),
        ),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, __: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response(message="Internal server error"),
    )


@app.get("/")
def health_check() -> dict[str, object]:
    db_connected = False

    try:
        db_connected = check_db_connection()
    except Exception:
        db_connected = False

    return success_response(
        data={"status": "ok", "database_connected": db_connected},
        message="Health check successful",
    )
