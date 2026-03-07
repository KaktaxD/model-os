from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Os(Base):
    __tablename__ = "os"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    version: Mapped[str] = mapped_column(String(20), nullable=False)
    release_year: Mapped[int] = mapped_column(Integer, nullable=False)
    # Один-ко-многим: одна OS → много Phone
    phones: Mapped[list["Phone"]] = relationship(
        "Phone",
        back_populates="os",
        cascade="all, delete-orphan"
    )
