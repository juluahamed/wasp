from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from wasp.database import Base

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	name = Column(String(50), nullable=False)
	email = Column(String(120), unique=True)
	picture = Column(String(250))
	time_created = Column(DateTime(timezone=True), server_default=func.now())
	time_updated = Column(DateTime(timezone=True), onupdate=func.now())
