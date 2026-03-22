from uuid import UUID

from sqlalchemy.orm import Session

from app.models.teacher import Teacher


def get_teachers_by_school(db: Session, school_id: UUID) -> list[Teacher]:
    return (
        db.query(Teacher)
        .filter(Teacher.school_id == school_id)
        .order_by(Teacher.name.asc())
        .all()
    )


def get_teacher_by_id(db: Session, teacher_id: UUID) -> Teacher | None:
    return db.query(Teacher).filter(Teacher.id == teacher_id).first()


def create_teacher(db: Session, school_id: UUID, data) -> Teacher:
    payload = data.model_dump() if hasattr(data, "model_dump") else dict(data)
    payload.pop("school_id", None)
    teacher = Teacher(school_id=school_id, **payload)
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher


def update_teacher(db: Session, teacher_id: UUID, data) -> Teacher | None:
    teacher = get_teacher_by_id(db, teacher_id)
    if teacher is None:
        return None

    payload = (
        data.model_dump(exclude_unset=True)
        if hasattr(data, "model_dump")
        else dict(data)
    )
    for field, value in payload.items():
        setattr(teacher, field, value)

    db.commit()
    db.refresh(teacher)
    return teacher


def delete_teacher(db: Session, teacher_id: UUID) -> bool:
    teacher = get_teacher_by_id(db, teacher_id)
    if teacher is None:
        return False

    db.delete(teacher)
    db.commit()
    return True
