from sqlalchemy import Column,String,Integer,ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id=Column(Integer,primary_key=True)
    username = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)
    notes = relationship("Note", back_populates="owner")

class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer,primary_key=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="notes")
