from flask import Flask, render_template, current_app, url_for, request, flash, redirect
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


# Allows you to use '%' for statements in templates as opposed to {%...%}
with app.app_context():
    current_app.jinja_env.line_statement_prefix = '%'


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant)
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new/', methods = ['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['newRestaurantName'])
        session.add(newRestaurant)
        session.commit()
        flash('New Restaurant Created!')
        return redirect(url_for('showRestaurants'))
    return render_template('newRestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return render_template('menu.html', items=items, restaurant_id = restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/edit/', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurants = session.query(Restaurant)
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        if request.form['editedRestaurantName']:
            restaurant.name = request.form['editedRestaurantName']
            session.add(restaurant)
            session.commit()
            flash('Restaurant Name Changed!')
        return redirect(url_for('showRestaurants'))
    return render_template('editRestaurant.html', restaurant = restaurant, restaurant_id = restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/delete/', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    return render_template('deleteRestaurant.html',
                           restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], course = request.form['course'],
                           price = request.form['price'], description = request.form['description'],
                           restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    return render_template('newMenuItem.html', restaurant_id = restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['course']:
            item.course = request.form['course']
        if request.form['price']:
            item.price = request.form['price']
        if request.form['description']:
            item.description = request.form['description']
        session.add(item)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    return render_template('editMenuItem.html',
                           restaurant_id = restaurant_id,
                           menu_id = menu_id,
                           item = item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods = ['POST', 'GET'])
def deleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Menu Item Deleted!')
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    return render_template('deleteMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = item)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
