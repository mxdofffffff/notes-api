from sqlalchemy import Column,String,Integer,ForeignKey,DateTime,Table
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import Boolean

note_tags = Table(
    'note_tags',
    Base.metadata,
    Column('note_id',Integer,ForeignKey('notes.id')),
    Column('tag_id',Integer,ForeignKey('tags.id'))
)

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    notes = relationship("Note", secondary = note_tags ,back_populates="tags")

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
    tags = relationship("Tag", secondary = note_tags ,back_populates="notes")
    created_at = Column(DateTime,default=datetime.utcnow)
    is_deleted = Column(Boolean,default=False)
    is_favorite = Column(Boolean,nullable = False,default = False)

class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    id = Column(Integer,primary_key=True)
    token = Column(String,unique=True,nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
