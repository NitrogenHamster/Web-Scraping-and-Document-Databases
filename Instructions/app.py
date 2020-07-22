  
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_data

# Use flask_pymongo to set up mongo connection
app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

# route
@app.route("/")
def index():
    mars_data = mongo.db.mars.find_one()

    return render_template("index.html", mars = mars_data)

@app.route("/scrape")
def scrape():
    
    mars = mongo.db.mars
    mars_data = scrape_data.Scrape()
    mars.update({}, mars_data, upsert=True)
    
    return redirect("http://localhost:5000/")

if __name__ == "__main__":
    app.run(debug=True)