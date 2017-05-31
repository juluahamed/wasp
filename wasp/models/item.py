from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from wasp.database import Base
from wasp.models import User, Category

class Item(Base):
	__tablename__ = 'items'

	id = Column(Integer, primary_key=True)
	name = Column(String(50), nullable=False)
	description = Column(Text, nullable=False)
	category_id = Column(Integer, ForeignKey('categories.id'))
	category = relationship(Category)
	user_id = Column(Integer, ForeignKey('users.id'))
	user = relationship(User)
	time_created = Column(DateTime(timezone=True), server_default=func.now())
	time_updated = Column(DateTime(timezone=True), onupdate=func.now())

	# Property to return a JSON serialized dictionary of db class
	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'description': self.description,
			'category_id': self.category_id,
			'category_name': self.category.name,
			'user_id': self.user_id,
			'user_name': self.user.name,
			'time_created': self.time_created,
			'time_updated': self.time_updated
		}