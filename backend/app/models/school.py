from datetime import datetime
from uuid import UUID as PyUUID, uuid4

from sqlalchemy import DateTime, Index, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class School(Base):
    __tablename__ = "schools"
    __table_args__ = (
        Index("ix_schools_district_upazila", "district", "upazila"),
        Index(
            "ix_schools_name_trgm",
            "name",
            postgresql_using="gin",
            postgresql_ops={"name": "gin_trgm_ops"},
        ),
    )

    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    emis_code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    country_code: Mapped[str] = mapped_column(String, default="BD", nullable=False, index=True)
    division: Mapped[str | None] = mapped_column(String(100), index=True, nullable=True)
    district: Mapped[str | None] = mapped_column(String(100), index=True, nullable=True)
    upazila: Mapped[str | None] = mapped_column(String(100), index=True, nullable=True)
    union: Mapped[str | None] = mapped_column(String(100), index=True, nullable=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    total_students: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_teachers: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
