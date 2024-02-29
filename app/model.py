import datetime

from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

from config_db import engine


class Base(DeclarativeBase):
    pass
    
  
class Ads(Base):
    __tablename__ = "ads"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1500))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    owner_id: Mapped[int] = mapped_column(Integer, nullable=False)
    
    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
        }


Base.metadata.drop_all(bind=engine) 
Base.metadata.create_all(bind=engine)      