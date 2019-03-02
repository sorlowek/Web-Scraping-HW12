from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

# setup mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app", connect=False)


@app.route("/")
def home():

     # Find one record of data from the mongo database
     mars_information = mongo.db.collection.find_one()
     return render_template("index.html",mars = mars_information)

@app.route("/scrape")
def scrape():

    # Run the scrape function
    final_mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, final_mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)