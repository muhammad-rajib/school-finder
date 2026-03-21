from datetime import datetime
from uuid import UUID as PyUUID, uuid4

from sqlalchemy import Boolean, DateTime, Index, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    website: Mapped[str | None] = mapped_column(String(255), nullable=True)
    established_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_students: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    boys: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    girls: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_teachers: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_classrooms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    has_electricity: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_water: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    images: Mapped[list["SchoolImage"]] = relationship("SchoolImage", back_populates="school")
    notices: Mapped[list["Notice"]] = relationship("Notice", back_populates="school")
    teachers: Mapped[list["Teacher"]] = relationship("Teacher", back_populates="school")
    results: Mapped[list["Result"]] = relationship("Result", back_populates="school")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
