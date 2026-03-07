from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Phone(Base):
    __tablename__ = "phones"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    firma: Mapped[str] = mapped_column(String(20), nullable=False)
    model: Mapped[str] = mapped_column(String(20), nullable=False)
    release_year: Mapped[int] = mapped_column(Integer, nullable=False)

    os_id: Mapped[int] = mapped_column(Integer, ForeignKey("os.id"), nullable=True)
    os = relationship("Os", back_populates="phones")



