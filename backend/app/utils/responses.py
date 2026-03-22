from typing import Any


def success_response(data: Any, message: str) -> dict[str, Any]:
    return {
        "success": True,
        "data": data,
        "message": message,
    }


def error_response(message: str, data: Any = None) -> dict[str, Any]:
    return {
        "success": False,
        "data": data,
        "message": message,
    }
