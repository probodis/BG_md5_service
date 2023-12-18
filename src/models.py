from datetime import datetime
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class UserFileOrm(Base):
    __tablename__ = "user_files"

    _id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[str] = mapped_column(nullable=False)
    file_id: Mapped[str] = mapped_column(nullable=False)
    md5: Mapped[Optional[str]]
    created: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
