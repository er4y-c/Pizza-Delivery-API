from db.database import Base, engine
from models.user import User
from models.order import Order

Base.metadata.create_all(bind=engine)