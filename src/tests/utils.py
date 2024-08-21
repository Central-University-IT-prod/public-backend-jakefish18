from sqlalchemy import MetaData, Table
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session
from sqlalchemy.schema import DropTable

from src.database import Base, engine




def clean_db():
    import src.models
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
