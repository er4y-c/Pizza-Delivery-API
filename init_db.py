from db.database import Base, engine
from models.models import User, Order

Base.metadata.create_all(bind=engine)