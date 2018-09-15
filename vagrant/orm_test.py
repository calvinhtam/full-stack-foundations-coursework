from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
#print(session.query(Restaurant).all())
#items = session.query(MenuItem).all()
#for item in items:
    #print(item.name)
veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for veggieBurger in veggieBurgers:
    print (veggieBurger.id, veggieBurger.price, veggieBurger.restaurant.name)
print('Urban Veggie Burger Update Time')
UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 20).one()
UrbanVeggieBurger.price = '$2.99'
session.add(UrbanVeggieBurger)
session.commit()
for veggieBurger in veggieBurgers:
    print (veggieBurger.id, veggieBurger.price, veggieBurger.restaurant.name)
print('Todos Burger Update Time')
for veggieBurger in veggieBurgers:
    print (veggieBurger.id, veggieBurger.price, veggieBurger.restaurant.name)
    if veggieBurger.price != '$2.99':
        veggieBurger.price = '$2.99'
        session.add(veggieBurger)
        session.commit()
        print ('Updated: ' + str(veggieBurger.id), veggieBurger.price, veggieBurger.restaurant.name)
spinachDessert = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
print(spinachDessert.restaurant.name)
session.delete(spinachDessert)
session.commit()
spinachDessert = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()

"""
#### creating restaurant and menuitem tutorial
testerRestaurant = Restaurant(name = 'Pizza Palace')
session.add(testerRestaurant)
session.commit()
veggiepizza = MenuItem(name = 'Veggie Pizza', description = 'Cheese and Veggies', course = 'Entree', price = '$10.99', restaurant = testerRestaurant)
session.add(veggiepizza)
session.commit()
print(session.query(MenuItem).all())
firstResult = session.query(Restaurant).first()
print(firstResult.name)
"""
