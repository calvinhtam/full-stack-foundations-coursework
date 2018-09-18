from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

session = scoped_session(sessionmaker(bind=engine))

@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurant=[i.serialize for i in restaurants])

@app.route('/restaurant/<int:restaurant_id>/JSON')
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItem=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
    return jsonify(MenuItem=item.serialize)

@app.teardown_request
def remove_session(ex=None):
    session.remove()

@app.route('/')
@app.route('/restaurant/')
@app.route('/restaurants/')
def showRestaurants():
    #return 'This page will show all my restaurants'
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    #return 'This page will add a new restaurant'
    restaurants = session.query(Restaurant).all()
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash('New Restaurant Created!')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html', restaurants=restaurants)

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    #return 'This page will edit the restaurant with the restaurant_id %s' % restaurant_id
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        flash("%s just edited!" % restaurant.name)
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    #return 'This page will delete the restaurant with the restaurant_id %s' % restaurant_id
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    #return 'This page will show the menu of the restaurant with the restaurant_id %s' % restaurant_id
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    appetizerItems = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, course='Appetizer')
    entreeItems = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, course='Entree')
    dessertItems = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, course='Dessert')
    beverageItems = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, course='Beverage')
    return render_template('showMenu.html', items=items, restaurant=restaurant, appetizerItems=appetizerItems,
                           entreeItems=entreeItems, dessertItems=dessertItems, beverageItems=beverageItems)

@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    #return 'This page will add a new menu item to the restaurant with the restaurant_id %s' % restaurant_id
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        newMenuItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id,
                               description=request.form['description'], price=request.form['price'],
                               course=request.form['course'])
        session.add(newMenuItem)
        session.commit()
        flash('New Menu Item Created!')
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    #return 'This page will edit the menu item with the menu_id %s at the restaurant with the restaurant_id %s' \
    #% (menu_id, restaurant_id)
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        editedItem.name = request.form['name'] if request.form['name'] else editedItem.name
        editedItem.description = request.form['description'] if request.form['description'] else editedItem.description
        editedItem.price = request.form['price'] if request.form['price'] else editedItem.price
        editedItem.course = request.form['course'] if request.form['course'] else editedItem.course
        session.add(editedItem)
        session.commit()
        flash("%s just edited!" % editedItem.name)
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    #return 'This page will delete the menu item with the menu_id %s at the restaurant with the restaurant_id %s' \
    #% (menu_id, restaurant_id)
    deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=deletedItem)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = '5000')