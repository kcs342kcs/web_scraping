from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scrape

# create instance of Flask app
app = Flask(__name__)

# mongoDB stuff
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

# drop collection if it exists
mongo.db.mars_facts.drop()

# create route that renders index.html template
@app.route("/")
def echo():
    mars_db_data = mongo.db.mars_facts.find_one()
    return render_template("index.html", mars_data=mars_db_data)
    # try:
    #     mars_db_data = mongo.db.mars_facts.find_one()
    #     return render_template("index.html", mars_data=mars_db_data)
    # except:
    #     return render_template("index.html")

@app.route('/scrape')
def scrape():
    # drop any existing mars data
    mongo.db.mars_facts.drop()

    # Run the scrape function
    mars_data = mars_scrape.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_facts.insert_one(mars_data)

    # Redirect back to home page
    return redirect("/")


    
if __name__ == "__main__":
    app.run(debug=True)
