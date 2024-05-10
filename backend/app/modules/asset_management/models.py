from uuid import uuid4

from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.common.mixins.timestamps import TimestampMixin
from app.modules.auth.models import User  # noqa: F401 > relationship 설정시 필요합니다.
from database.config import MySQLBase


class Stock(TimestampMixin, MySQLBase):
    __tablename__ = "stocks"

    @staticmethod
    def get_uuid():
        return str(uuid4())

    id = Column(String(36), primary_key=True, default=get_uuid)
    code = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    market_index = Column(String(255), nullable=False)
    date = Column(Date, nullable=False, info={"description": "stock closing day"})
    opening_price = Column(Float, nullable=False, info={"description": "Opening price of the stock"})
    highest_price = Column(Float, nullable=False, info={"description": "Highest price of the stock"})
    lowest_price = Column(Float, nullable=False, info={"description": "Lowest price of the stock"})
    close_price = Column(Float, nullable=False, info={"description": "Closing price of the stock"})
    adj_close_price = Column(Float, nullable=False, info={"description": "Adjusted closing price of the stock"})
    trade_volume = Column(Integer, nullable=False, info={"description": "Volume of stock traded"})

    transactions = relationship("StockTransaction", back_populates="stock")


class StockTransaction(TimestampMixin, MySQLBase):
    __tablename__ = "stock_transactions"

    @staticmethod
    def get_uuid():
        return str(uuid4())

    id = Column(String(36), primary_key=True, default=get_uuid)
    quantity = Column(Integer, nullable=False)
    investment_bank = Column(String(255), nullable=False)
    stock_id = Column(String(36), ForeignKey("stocks.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="transactions")
    stock = relationship("Stock", back_populates="transactions")
