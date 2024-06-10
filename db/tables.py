import datetime

from sqlalchemy import Column, Integer, String, Float, TIMESTAMP

from db.connection import Base


class OrderBookDB(Base):
    __tablename__ = 'order_book'
    __table_args__ = {
        'extend_existing': True,
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Float)
    volume = Column(Float)
    full_volume = Column(Float)
    type = Column(String)
    last_updated_id = Column(String)
    symbol = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now)
