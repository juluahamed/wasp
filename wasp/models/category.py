from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from wasp.database import Base
from wasp.models import User
from flask import url_for

class Category(Base):
	__tablename__ = 'categories'

	id = Column(Integer, primary_key=True)
	name = Column(String(50), nullable=False)
	user_id = Column(Integer, ForeignKey('users.id'))
	picture = Column(String(100), default='default_cat_image.png')
	user = relationship(User)
	time_created = Column(DateTime(timezone=True), server_default=func.now())
	time_updated = Column(DateTime(timezone=True), onupdate=func.now())

	# Property to return a JSON serialized dictionary of db class
	@property
	def serialize(self):
		return{
			'id': self.id,
			'name': self.name,
			'picture': self.picture,
			'user_id': self.user_id,
			'user_name': self.user.name,
			'time_created': self.time_created,
			'time_updated': self.time_updated,
			'pic_url': url_for('uploadedFile', filename=self.picture)
		}