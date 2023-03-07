from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine('sqlite:///dungeonstuff.db')

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)