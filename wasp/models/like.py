from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from wasp.database import Base
from wasp.models import User, Category, Item

class Like(Base):
	__tablename__ = 'likes'

	id = Column(Integer, primary_key=True)
	category_id = Column(Integer, ForeignKey('categories.id'))
	category = relationship(Category)
	item_id = Column(Integer, ForeignKey('items.id'))
	item = relationship(Item)
	user_id = Column(Integer, ForeignKey('users.id'))
	user = relationship(User)
	time_created = Column(DateTime(timezone=True), server_default=func.now())
	time_updated = Column(DateTime(timezone=True), onupdate=func.now())

	# Property to return a JSON serialized dictionary of db class
	@property
	def serialize(self):
		return {
			'id': self.id,
			'category_id': self.category_id,
			'category_name': self.category.name,
			'item_id': self.item_id,
			'item_name': self.item.name,
			'user_id': self.user_id,
			'time_created': self.time_created,
			'time_updated': self.time_updated
		}