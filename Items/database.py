from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///dungeonstuff.db')

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

class DungeonStuff(Base):
    __tablename__ = 'dungeonstuff'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Weapons(Base):
    __tablename__ = 'weapons'
    id = Column(Integer, primary_key=True)
    dungeonstuff_id = Column(Integer, ForeignKey('dungeonstuff.id'))
    damage = Column(Integer)
    durability = Column(Integer)
    dungeonstuff = relationship('DungeonStuff', backref='weapons')

Base.metadata.create_all(engine)

weapon_data = {
    "Dagger": {"price": 25, "damage": 15},
    "Sword": {"price": 50, "damage": 20},
    "Axe": {"price": 100, "damage": 25},
    "Bow": {"price": 200, "damage": 30},
}

for name, data in weapon_data.items():
    dungeonstuff = DungeonStuff(name=name)
    weapon = Weapons(dungeonstuff=dungeonstuff, damage=data["damage"])
    session.add(weapon)

session.commit()

stmt = session.query(Weapons).all()
for row in stmt:
    print(row.dungeonstuff.name, row.damage, row.durability)