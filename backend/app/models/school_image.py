from datetime import datetime
from uuid import UUID as PyUUID, uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class SchoolImage(Base):
    __tablename__ = "school_images"

    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    school_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schools.id"),
        index=True,
        nullable=False,
    )
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    is_cover: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    school: Mapped["School"] = relationship("School", back_populates="images")
