from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo

# From the separate python file directory import the code to scrape pages
from scrape_mars import scrape

app = Flask(__name__)

# Flask_pymongo for mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/Mission-to-Mars"
mongo = PyMongo(app)

# Collection
mars_data = mongo.db.mars_data
# Mars_data.drop()

# Render the index.html page with any craigslist listings in database.
# In case of no listings, the table remain empty.
@app.route("/")
def index():
    mars_info = mars_data.find_one()
    print(mars_info)
    return render_template("index.html", data_db=mars_info)


# This process will trigger the webscraping and then
# send back to the index route to render the results
@app.route("/scrape")
def scraper():

    # drop collection
    mars_data.drop()

    # scrape_craigslist.scrape() and
    # defined in the scrape_mars.py file within this directory
    scraped_data = scrape()
    mars_data.insert_many([scraped_data])

    # Flask's function to send to a
    # different route after task completed
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)