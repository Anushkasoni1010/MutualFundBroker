from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class UserPortfolio(Base):
    __tablename__ = 'user_portfolio'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    fund_house = Column(String)
    scheme_code = Column(String)
    scheme_name = Column(String)
    units = Column(Float)
    purchase_date = Column(DateTime, default=datetime.now(timezone.utc))

class NAV(Base):
    __tablename__ = "navs"

    scheme_code = Column(String, primary_key=True)
    nav = Column(Float)
    last_updated = Column(DateTime)

