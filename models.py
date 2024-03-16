from database import Base
from sqlalchemy import Column, Integer, String, Boolean


class ToDo(Base):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complite = Column(Boolean, default=False)

