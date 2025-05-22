from models import Base
from datetime import datetime

from sqlalchemy import String, Text, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    summary: Mapped[str | None] = mapped_column(Text)
    published: Mapped[datetime | None] = mapped_column(DateTime)
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String))
