from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    title = Column(
        String,
        nullable=False,
    )

    description = Column(
        String,
        nullable=False,
    )

    status = Column(
        String,
        nullable=False,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    )

    duration = Column(
        Integer,
        nullable=True,
    )

    created_by = Column(
        String,
        nullable=True,
    )

    user = relationship(
        "User",
        back_populates="videos",
    )