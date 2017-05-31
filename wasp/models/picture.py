from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from wasp.database import Base
from wasp.models import User, Item
from flask import url_for

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

	# Property to return a JSON serialized dictionary of db class
	@property
	def serialize(self):
		return{
			'id': self.id,
			'name': self.name,
			'item_id': self.item_id,
			'item_name': self.item.name,
			'user_id': self.user_id,
			'user_name': self.user.name,
			'time_created': self.time_created,
			'time_updated': self.time_updated,
			'pic_url': url_for('uploadedFile', filename=self.name)
		}