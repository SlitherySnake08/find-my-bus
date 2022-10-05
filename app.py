from flask import Flask, render_template, request, redirect
import json
from datetime import date

app = Flask(__name__)

towns = ['Allendale / Glen Rock/Midland Park/ Waldwick','Becton Regional  - Becton/Carlstadt/East Rutherford/Woodridge','Bogota / Moonachie/South Hackensack','Bergenfield/New Milford','Cliffside Park/Fairview/Palisades Park','Dumont/Cresskill','Edgewater / Leonia','Elmwood Park/ Hasbrouck Heights','Englewood / Tenafly','Englewood Cliffs','Fair Lawn','Fort Lee', 'Garfield','Franklin Lakes/Oakland','Hackensack / Oradell / River Edge','Hohokus','Lodi','Lyndhurst / North Arlington','Mahwah (1) Mahwah / Franklin Lakes/Wykoff','Mahwah (2) Mahwah/Ramsey','Maywood','Northern Valley/ Old Tappan/ Demarest/ Closter/ Harrington Park/ Haworth/ Norwood/Northvale)',  'Paramus','Pascack Valley / Park Ridge / Hillsdale / Montvale / Rivervale / Woodcliff Lake / Westwood','Ridgefield','Ridgefield Park / Little Ferry','Ridgewood/ Rochelle Park/Saddle Brook','Rutherford / Wallington','Teaneck', 'Upper Saddle River']
companies = ['Leckie (TT004)','Becton','Leckie (TT227)','Bergenfield','Cliffside','Dumont','Leonia','Joshua Tours (TT221)','Englewood','Leckie (TT204)','Joshua Tours (TT222)','Joshua Tours (TT205)','Garfield','D&M (TT001)','Joshua Tours (TT224)','N&Y Transportation','Leckie (TT220)','Leckie (TT202)','Leckie (TT002)','Leckie (TT006)','Leckie (TT231)','Valley (VA326)','First Student (TT001)','Leckie (TT003). ',          'First Student (TET11)','Ridgefield Park','Joshua Tours (TT228)','Joshua Tours (TT226)','Teaneck','Leckie (TT005)']

@app.route('/')
def home():
    with open('static/change.txt', 'r') as file:
        past_date = file.read()
        if past_date != str(date.today()):
            with open('static/buses.json', 'w') as file:
                file.write('{}')
    return render_template('index.html')

@app.route('/bus-view')
def bus_view():
    with open('static/buses.json') as file:
        buses = json.load(file)
    return render_template('bus-view.html', list=buses)

@app.route('/authenticate/', methods=['POST', 'GET'], defaults={'result':None})
@app.route('/authenticate/<string:result>', methods=['POST', 'GET'])
def authenticate(result):
    if request.method == 'GET':
        return render_template('authenticate.html', result = result)
    if request.method == 'POST':
        password = request.form['admin_pass']
        if password == '1234':
            return redirect('/add?login=true')
        else: 
            return redirect('/authenticate/incorrect')
    
@app.route('/add', methods=['GET', 'POST'], defaults={'result':None})
@app.route('/add/<string:result>', methods=['GET', 'POST'])
def add_bus(result):
    if request.method == 'GET':
        if request.args.get('login') == 'true':
            return render_template('add.html', towns=towns, result=result)
        else:
            return redirect('/authenticate')
    elif request.method == 'POST':
        with open('static/buses.json') as file:
            current_buses = json.load(file)
        bus_town = request.form['town']
        if bus_town == 'Town':
            return redirect('/add/error?login=true')
        index = towns.index(bus_town)
        bus_company = companies[index]
        spot = request.form['spot']
        if spot == '':
            return redirect('/add/error?login=true')
        arrived = request.form['arrived']
        if arrived == 'Arrived?':
            return redirect('/add/error?login=true')
        lastcall = request.form['lastcall']
        if lastcall == 'Last Call?':
            return redirect('/add/error?login=true')
        departed = request.form['departed']
        if departed == 'Departed?':
            return redirect('/add/error?login=true')
        bus_data = {"town":bus_town, "company":bus_company, "spot":spot, "arrived":arrived, "lastcall":lastcall, "departed":departed}
        current_buses[bus_town] = bus_data
        json_object = json.dumps(current_buses, indent=4)
        with open("static/buses.json", "w") as outfile:
            outfile.write(json_object)
        with open('static/change.txt', 'w') as file:
            file.write(str(date.today()))
        return redirect('/add/good?login=true')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)