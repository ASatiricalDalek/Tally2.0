import sqlite3 as sql
import importlib.util, sys
from flask import Flask, render_template, request
import importlib.util
from datetime import datetime
# Import the database.py file. Have to specify its full path
spec = importlib.util.spec_from_file_location("database", "/var/www/tally2/tally2/database.py")
dbpy = importlib.util.module_from_spec(spec)
# Database.py is now aliased as dbpy
spec.loader.exec_module(dbpy)

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def mainpage():
    # If the form isn't submitted, postMsg still gets returned
    # Initialize to None to avoid errors, and an empty message
    postMsg = None
    if request.method == 'POST':
        # If please select is selected, don't say anything posted to the DB
        # No reason to run the query either, though it does check for this
        if request.form['questionType'] != "999":
            dbpy.markTally()
            qtype = request.form['questionType']
            today = datetime.now().strftime('%m-%d-%y %-I:%M %p')
            postMsg = qtype + " successfully posted at " + str(today)
        
        
    return render_template("index.html", postMsg = postMsg)

# POST is the method to get the form data, GET is the method to view the page
# If GET isn't included the page won't load.
@app.route("/reports", methods=['POST', 'GET']) 
def report():
    # Used to set the date boxes to the current day when page is loaded
    niceDay = dbpy.getToday()
    # If the method is post we know the user just submitted the form, try and populate the table
    if request.method == 'POST':
        questionInfo = dbpy.query('tallyType')
        if questionInfo[0] is None:
            return render_template("reports.html", qtype_verbose = questionInfo[1], niceDay = niceDay)
        else:
            return render_template("reports.html", questions = questionInfo[0], qtype_verbose = questionInfo[1], start = questionInfo[2], end = questionInfo[3], advanced = questionInfo[4], niceDay = niceDay)
        # Values are returned as a list from the query functions as there are many.
        
    # Otherwise, the user probably just opened the page, so don't try and populate the table
    # just display the page
    else:
        return render_template("reports.html", niceDay = niceDay)


if __name__ == "__main__":
	app.run()
