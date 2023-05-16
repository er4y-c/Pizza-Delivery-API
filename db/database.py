from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dynaconf import settings
engine = create_engine(settings.POSTGRE_SQL_URL, echo=True)

Base = declarative_base()
Session = sessionmaker()
