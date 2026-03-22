from uuid import UUID

from sqlalchemy.orm import Session

from app.models.result import Result


def get_result_by_id(db: Session, result_id: UUID) -> Result | None:
    return db.query(Result).filter(Result.id == result_id).first()


def create_result(db: Session, school_id: UUID, data) -> Result:
    payload = data.model_dump() if hasattr(data, "model_dump") else dict(data)
    payload.pop("school_id", None)
    result = Result(school_id=school_id, **payload)
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


def update_result(db: Session, result_id: UUID, data) -> Result | None:
    result = get_result_by_id(db, result_id)
    if result is None:
        return None

    payload = (
        data.model_dump(exclude_unset=True)
        if hasattr(data, "model_dump")
        else dict(data)
    )
    for field, value in payload.items():
        setattr(result, field, value)

    db.commit()
    db.refresh(result)
    return result


def delete_result(db: Session, result_id: UUID) -> bool:
    result = get_result_by_id(db, result_id)
    if result is None:
        return False

    db.delete(result)
    db.commit()
    return True


def get_results_by_school(db: Session, school_id: UUID) -> list[Result]:
    return (
        db.query(Result)
        .filter(Result.school_id == school_id)
        .order_by(Result.year.desc(), Result.exam_type.asc())
        .all()
    )
