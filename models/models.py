from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .db import Base

class VM(Base):
    __tablename__ = "vms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    image = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
