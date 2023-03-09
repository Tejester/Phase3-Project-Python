from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from models import Base, Score



engine = create_engine('sqlite:///dungeonstuff.db')

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
Base.metadata.append(Score.__table__)
