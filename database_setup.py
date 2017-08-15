# SQLAlchemy Notes
#
# Configuration - what we use to import all necessary modules
# *sets up all dependencies and binds code to SQLAlchemy engine
# *doesn't change much from project to project
# *creates instance of declarative base
#
# Class - code used to represent data in python
# *extends the base class
# *nested inside will be table and mapper code
#
# Table - represents a specific table in the database
# *syntax - __tablename__ = 'some_table'
#
# Mapper - connects columns of a table to the class that represents it
# *creates variables that we will use to create columns in our database
# *when column is created, you must also pass in attributes of that column
#

import sys

# these will come in handy when writing mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

# to be used in configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# helps create foreign key relationships
from sqlalchemy.orm import relationship

# we will use this in our configuration code at the end of the file
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
	__tablename__ = 'restaurant'
	
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)

class MenuItem(Base):
	__tablename__ = 'menu_item'

	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)