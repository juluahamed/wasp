from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from wasp.database import Base
from wasp.models import User, Item

class Picture(Base):
	__tablename__ = 'pictures'

	id = Column(Integer, primary_key=True)
	name = Column(String(50), nullable=False)
	item_id = Column(Integer, ForeignKey('items.id'))
	item = relationship(Item)
	user_id = Column(Integer, ForeignKey('users.id'))
	user = relationship(User)
	time_created = Column(DateTime(timezone=True), server_default=func.now())
	time_updated = Column(DateTime(timezone=True), onupdate=func.now())