# Configuration Code:
# sets up all "dependencies" needed for database and binds code to
# SQLAlchemy engine
"""
import sys

#(mapper code)
from sqlalchemy import Column, ForeignKey, Integer, String
#inherit features of SQLAlchemy (configuration and class code)
from sqlalchemy.ext.declarative import declarative_base
#(mapper code)
from sqlalchemy.orm import relationship
#end for connecting/configuring at end of config.code
from sqlalchemy import create_engine

Base = declarative_base()



#end of config section:
#create database being used (new file)
engine = create_engine('sqlite:///restaurantmenu.db')

#adds classes as tables in database
Base.metadata.create_all(engine)
"""

##########
# Class Code:
# object-oriented representation of tables in database
# beginning and end of config code
"""
class Restaurant(Base):

class MenuItem(Base):
"""

##########
# Table Code:
# representation of tables in database
# in class code
"""
#in Restaurant class
__tablename__ = 'restaurant'
#in MenuItem class 
__tablename__ = 'menu_item'
"""

##########
# Mapper Code:
# columns in database
"""
#Restaurant class
#string max length = 80, requires a value
name = Column (String(80), nullable = False)
#integer, id = primary key
id = Column (Integer, primary_key = True)

#MenuItem class
#string max length 80, requires a value
name - Column (String(80), nullable = False)
#string max length 250
course = Column (String(250))
# ^^
description = Column (String(250))
# ^^ 8
price = Column (String(8))
#integer, foreign key reference to restaurant id
restaurant_id = Column (Integer, ForeignKey('restaurant.id'))
#restaurant class relationship
restaurant = relationship(Restaurant)
"""

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
