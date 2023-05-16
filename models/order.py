from db.database import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType

class Order(Base):
    __tablename__ = "orders"

    ORDER_STATUS_TYPES = {
      ("0", "Hazırlanıyor"),
      ("1", "Yola çıktı"),
      ("2", "Teslim edildi")
    }

    PIZZA_TYPES = {
      ("S","Küçük Boy"),
      ("M", "Orta Boy"),
      ("L", "Büyük Boy")
    }
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices=ORDER_STATUS_TYPES), default="0")
    pizza_sizes = Column(ChoiceType(choices=PIZZA_TYPES), default="S")
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="orders")

    def __repr__(self):
        return f"Order {self.id}"  