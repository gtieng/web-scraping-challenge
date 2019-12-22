#import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Set route
@app.route('/')
def index():

    # Find one record of data from the mongo database
    mars_data = mongo.db.mars.find_one()
    
    # Return the template with the teams list passed in
    return render_template('index.html', content=mars_data)

# Set route
@app.route('/scrape')
def action():

    scrape = scrape_mars.scrape()

    mongo.db.mars.update({}, scrape, upsert=True)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)