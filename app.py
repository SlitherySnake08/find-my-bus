'''The purpose of this webapp is to create an app to manage buses and inform students'''
from datetime import date
import sqlite3
from flask import Flask, render_template, request, redirect

# open the database connection and define cursor. Create table and close connection
conn = sqlite3.connect('static/buses_database.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS buses(
          town text,
          company text,
          spot text,
          arrived text,
          lastcall text,
          departed text,
          date text
)""")



def check_date():
    '''
    check the date of the last edit made.
    If it doens't match, delete contents of buses, because a new day has passed.
    '''
    conn = sqlite3.connect('static/buses_database.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM buses")
    records = c.fetchall()
    print(records)
    print(len(records))
    if len(records) != 0:
        if records[0][-2] != str(date.today()):
            print(records[0][-2])
            print(date.today())
            c.execute("DELETE FROM buses")
            conn.commit()
            conn.close()
    # print(records)
    
    


def add_to_db(town, spot, arrived, lastcall, departed):
    '''
    Open database, and get company name of bus.
    Insert the bus into the database, and close connection
    '''
    conn = sqlite3.connect('static/buses_database.db')
    c = conn.cursor()
    index = towns.index(town)
    company = companies[index]
    c.execute(
        "INSERT INTO buses VALUES (:town, :company, :spot, :arrived, :lastcall, :departed, :date)",
              {
                  'town': town,
                  'company': company,
                  'spot': spot,
                  'arrived': arrived,
                  'lastcall': lastcall,
                  'departed': departed,
                  'date': str(date.today())
              })
    conn.commit()
    conn.close()


def show_buses():
    '''
    display all buses in table
    '''
    conn = sqlite3.connect('static/buses_database.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM buses")
    records = c.fetchall()
    conn.commit()
    conn.close()
    return records


def edit_bus(oid, spot, arrived, lastcall, departed):
    '''
    edit a bus by using the id of the bus and replacing new info
    '''
    conn = sqlite3.connect('static/buses_database.db')
    c = conn.cursor()
    c.execute(f"UPDATE BUSES SET 'spot' = '{spot}' where oid = '{oid}'")
    c.execute(f"UPDATE BUSES SET 'arrived' = '{arrived}' where oid = '{oid}'")
    c.execute(
        f"UPDATE BUSES SET 'lastcall' = '{lastcall}' where oid = '{oid}'")
    c.execute(
        f"UPDATE BUSES SET 'departed' = '{departed}' where oid = '{oid}'")
    conn.commit()
    conn.close()


app = Flask(__name__)

towns = ['Allendale / Glen Rock/Midland Park/ Waldwick',
         'Becton Regional  - Becton/Carlstadt/East Rutherford/Woodridge',
         'Bogota / Moonachie/South Hackensack', 'Bergenfield/New Milford',
         'Cliffside Park/Fairview/Palisades Park', 'Dumont/Cresskill',
         'Edgewater / Leonia', 'Elmwood Park/ Hasbrouck Heights', 'Englewood / Tenafly',
         'Englewood Cliffs', 'Fair Lawn', 'Fort Lee', 'Garfield', 'Franklin Lakes/Oakland',
         'Hackensack / Oradell / River Edge', 'Hohokus', 'Lodi', 'Lyndhurst / North Arlington',
         'Mahwah (1) Mahwah / Franklin Lakes/Wykoff', 'Mahwah (2) Mahwah/Ramsey', 'Maywood',
         'Northern Valley/Old Tappan/Demarest/Closter/Harrington Park/Haworth/Norwood/Northvale)',
         'Paramus',
         'Pascack Valley/Park Ridge/Hillsdale / Montvale / Rivervale / Woodcliff Lake / Westwood',
         'Ridgefield', 'Ridgefield Park / Little Ferry', 'Ridgewood/ Rochelle Park/Saddle Brook',
         'Rutherford / Wallington', 'Teaneck', 'Upper Saddle River']
companies = ['Leckie (TT004)', 'Becton', 'Leckie (TT227)', 'Bergenfield', 'Cliffside', 'Dumont',
             'Leonia', 'Joshua Tours (TT221)', 'Englewood', 'Leckie (TT204)',
             'Joshua Tours (TT222)',
             'Joshua Tours (TT205)', 'Garfield', 'D&M (TT001)', 'Joshua Tours (TT224)',
             'N&Y Transportation', 'Leckie (TT220)', 'Leckie (TT202)', 'Leckie (TT002)',
             'Leckie (TT006)', 'Leckie (TT231)', 'Valley (VA326)', 'First Student (TT001)',
             'Leckie (TT003). ', 'First Student (TET11)',
             'Ridgefield Park', 'Joshua Tours (TT228)', 'Joshua Tours (TT226)',
             'Teaneck', 'Leckie (TT005)']


@app.route('/')
def home():
    '''
    home screen, pretty self-explanatory. Also checks date.
    '''
    # with open('static/change.txt', 'r') as file:
    #     past_date = file.read()
    #     if past_date != str(date.today()):
    #         with open('static/buses.json', 'w') as file:
    #             file.write('{}')
    check_date()
    return render_template('index.html')


@app.route('/bus-view')
def bus_view():
    '''
    Screen that displays buses
    '''
    buses = show_buses()
    return render_template('bus-view.html', list=buses)


@app.route('/authenticate/', methods=['POST', 'GET'], defaults={'result': None})
@app.route('/authenticate/<string:result>', methods=['POST', 'GET'])
def authenticate(result):
    '''
    Admin authentication page.
    Check if password is correct for post request,
    otherwise, just display with result of past test.
    '''
    if request.method == 'GET':
        return render_template('authenticate.html', result=result)
    password = request.form['admin_pass']
    if password == '1234':
        return redirect('/add?login=true')
    return redirect('/authenticate/incorrect')


@app.route('/add', methods=['GET', 'POST'], defaults={'result': None})
@app.route('/add/<string:result>', methods=['GET', 'POST'])
def add_bus(result):
    '''
    If get request, display result of adding buses
    If not, get data from form, check if entered properly,
    check if data needs to be updated or added, and do respective function
    '''
    if request.method == 'GET':
        if request.args.get('login') == 'true':
            return render_template('add.html', towns=towns, result=result)
        return redirect('/authenticate')
    town = request.form['town']
    spot = request.form['spot']
    arrived = request.form['arrived']
    lastcall = request.form['lastcall']
    departed = request.form['departed']

    def redirect_error():
        return redirect('/add/error?login=true')
    # check each value for proper entry
    if town == 'Town':
        redirect_error()
    if spot == '':
        redirect_error()
    if arrived == 'Arrived?':
        redirect_error()
    if lastcall == 'Last Call?':
        redirect_error()
    if departed == 'Departed?':
        redirect_error()
    # if passed, check if data needs to be updated
    current_buses = show_buses()
    type_of_edit = 'new'
    index = 0
    for i in current_buses:
        if i[0] == town:
            # update value
            type_of_edit = 'update'
            index = current_buses.index(i)
    # print(type_of_edit)
    # print(index)
    if type_of_edit == 'new':
        add_to_db(town, spot, arrived, lastcall, departed)
    elif type_of_edit == 'update':
        edit_bus(index+1, spot, arrived, lastcall, departed)
    # after_edit = show_buses()
    # print(show_buses())
    # print(after_edit)
    return redirect('/add/good?login=true')

# close database
conn.commit()
conn.close()

# run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
