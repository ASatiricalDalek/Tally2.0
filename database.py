import importlib.util
import sqlite3 as sql
from flask import request
from datetime import datetime
# Import the logger file using its full path, aliased as log
spec = importlib.util.spec_from_file_location("database", "/var/www/tally2/tally2/logger.py")
log = importlib.util.module_from_spec(spec)
spec.loader.exec_module(log)

# Database location on server
DATABASE = '/var/www/tally2/tally2.db'

def query(formControl):
    con = sql.connect(DATABASE)
    con.row_factory = sql.Row
    cur = con.cursor()
    # Form control is the name of the object on the HTML page where the type of question we are tallying is defined
    # For this application, this is usually the tallyType combo box
    qtype = request.form[formControl]
    startDate = request.form["start"]
    endDate = request.form["end"]
    dates = pythonDate(startDate, endDate)
    startDate = dates[0]
    endDate = dates[1]
    
    adv = request.form.get('chkadv')
    
    if adv is not None:
        log.writeTallyLog("Running Advanced Query")
        advanced = True
        questions = advancedQuery(con, cur, qtype, startDate, endDate)
    else:
        log.writeTallyLog("Running Simple Query")
        advanced = False
        questions = simpleQuery(con, cur, qtype, startDate, endDate)
    
    # So 999 doesn't get printed as the table header if run report is clicked w/o selecting a question
    if qtype == "999":
        qtype = "Please select a type of question"
        
    # Return the question count, the header and start and end dates, nicely formatted. 
    # Also the advaned bool which tells what HTML table to display
    return [questions, qtype, startDate.strftime('%m-%d-%y %-I:%M %p'), endDate.strftime('%m-%d-%y %-I:%M %p'), advanced]

def simpleQuery(con, cur, qtype, startDate, endDate):
    if qtype == "All Interactions":
        cur.execute("SELECT COUNT(tally_id), time FROM tally WHERE time >= ? AND time <= ?", (startDate, endDate))
    # The value of 999 from the combo box is the placeholder "Please Select"
    elif qtype == "999":
        questions = None
    else:
        cur.execute("SELECT COUNT(tally_id), time FROM tally WHERE tally_id = ? AND time >= ? AND time <= ?", (qtype, startDate, endDate))
        # qType is both the value from the dropdown box and the value saved in the db
        
    # Once the query is run, we have to fetch the results to save them to a variable
    questions = cur.fetchall();
    if questions is None:
        questions = "No Results" 
        
    return questions

def advancedQuery(con, cur, qtype, startDate, endDate):
    if qtype == "All Interactions":
        cur.execute("SELECT tally_id, time FROM tally WHERE time >= ? AND time <= ? ORDER BY tally_id, time", (startDate, endDate))
    elif qtype == "999":
        questions = None
    else:
        cur.execute("SELECT tally_id, time FROM tally WHERE tally_id = ? AND time >= ? AND time <= ? ORDER BY tally_id, time", (qtype, startDate, endDate))
        
    questions = cur.fetchall();
    if questions is None:
        questions = "No Results"
    
    return questions

# Convert string into a nicer date time format    
def pythonDate(formStartDate, formEndDate):
    pythonStartDate = datetime.strptime(formStartDate, '%Y-%m-%dT%H:%M')
    pythonEndDate = datetime.strptime(formEndDate, '%Y-%m-%dT%H:%M')
    return [pythonStartDate, pythonEndDate]

# Returns today in YYYY-mm-dd format, for populating the date selection boxes
def getToday():
    niceDay = datetime.now().strftime('%Y-%m-%d')
    return niceDay

def markTally():
    con = sql.connect(DATABASE)
    con.row_factory = sql.Row
    cur = con.cursor()
    
    # We need hours and minutes but not seconds or microseconds
    stamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    question = request.form['questionType']
    if question == "999":
        log.writeTallyLog("No question type selected, ignoring")
    else:
        log.writeTallyLog("Recording tally for " + question + " at time " + str(stamp))
        cur.execute("INSERT INTO tally VALUES(?,?)", (question, stamp))
        con.commit()
        log.writeTallyLog("Values successfully recorded")
    