import time

from sqlalchemy import text

from app.db.session import engine


def wait(max_retries: int = 10, retry_delay: int = 2) -> None:
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return
        except Exception as exc:
            last_error = exc
            if attempt == max_retries:
                break
            time.sleep(retry_delay)

    raise RuntimeError("Database is not ready after maximum retries") from last_error
