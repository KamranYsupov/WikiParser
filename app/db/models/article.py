import uuid
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey

from app.db.models.base import Base
from app.db.models.mixins import UUIDMixin, TimestampedMixin


class Article(Base, UUIDMixin, TimestampedMixin):
    """Модель статьи"""
    title: Mapped[str] = mapped_column(String, unique=True, index=True)
    url: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(Text)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
