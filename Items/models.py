from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Weapon(Base):
    __tablename__ = 'weapons'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    damage = Column(Integer)


class Hero(Base):
    __tablename__ = 'heroes'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    health = Column(Integer)
    damage = Column(Integer)

class Enemy(Base):
    __tablename__ = 'enemies'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    health = Column(Integer)
    damage = Column(Integer)
    gold = Column(Integer)

class Trap(Base):
    __tablename__ = 'traps'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    damage = Column(Integer)

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    name = Column(String)