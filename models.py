from sqlalchemy import create_engine, Column, String, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os


db_url = os.environ.get('DATABASE_URL') or "sqlite:///app.db"
engine = create_engine(db_url, echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    name = Column(String, primary_key=True)
    password = Column(String)

    posts = relationship("Todo", backref="users")

    def __repr__(self):
        return "<name={} password={}>".format(self.name, self.password)


class Todo(Base):
    __tablename__ = "todos"


    id = Column(Integer, primary_key=True)
    name = Column(String, ForeignKey("users.name"))
    date = Column(String)
    body = Column(String)

    user = relationship("User")
    



Base.metadata.create_all(engine)
SessionMaker = sessionmaker(bind=engine)


session = SessionMaker()


