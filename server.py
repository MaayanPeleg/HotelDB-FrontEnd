#run "pip install mysql-connector-python flask markupsafe"
# run with "flask --app server run --debug"
from flask import Flask, request, render_template
import mysql.connector as mysql
import requests
from markupsafe import Markup
import urllib3
import os

app = Flask(__name__)

API = os.environ.get('API_URL')

API = f'http://{API}'

def check_connection():
    #checks if connection can be made with timeout of 5 seconds
    try:
        http = urllib3.PoolManager()
        http.request('GET', API)
        return True
    except:
        return False

@app.route('/reservation/')
def reservation():
    #Connect to db
    #check if connection can be made

    if check_connection() == False:
        HTMLOut = '<div class="card" style="width: 40rem;">'
        HTMLOut += f'<div class="card-header text-center">Error: Could not connect to API</div>'
        HTMLOut += f'</div>'

        HTMLOut = Markup(HTMLOut)
        return render_template('index.html', content=HTMLOut)


    with requests.get(f'{API}/reservation/') as r:
        data = r.json()
        #OUtput
        HTMLOut = '<div class="card" style="width: 40rem;">'
        HTMLOut += f'<div class="card-header text-center">Reservations</div>'
        HTMLOut += f'<ul class="list-group list-group-flush">'
        #For all reservations
        for res in data['reservations']:
            #sets variables to make code more understandable
            resid = res["ReservationID"]
            startdate = res["StartDate"]
            enddate = res["EndDate"]
            name = f'{res["FirstName"]} {res["LastName"]}'
            guestid = res["GuestID"]

            #Generates HTML
            HTMLOut += '<li class="list-group-item"><ul style="list-style: none">'
            HTMLOut += f'<li><b>ReservationID:</b> <a class="btn btn-outline-secondary" role="button" href="/reservation/search?reservationid={resid}">{resid}</a></li>'
            HTMLOut += f'<li><b>Start Date:</b> {startdate} </li>'
            HTMLOut += f'<li><b>End Date:</b> {enddate} </li>'
            HTMLOut += f'<li><b>Guest:</b> <a class="btn btn-outline-secondary" role="button" href="/guest/search?guestid={guestid}">{name}</a></li>'
            HTMLOut += '</ul></li>'

        HTMLOut += f'</ul></div>'
        #displays HTML
        HTMLOut = Markup(HTMLOut)

        return render_template('index.html', content=HTMLOut)

@app.route('/reservation/search', methods=['GET'])
def get_reservation():

    #check if connection can be made

    if check_connection() == False:
        HTMLOut = '<div class="card" style="width: 40rem;">'
        HTMLOut += f'<div class="card-header text-center">Error: Could not connect to API</div>'
        HTMLOut += f'</div>'

        HTMLOut = Markup(HTMLOut)
        return render_template('index.html', content=HTMLOut)

    args = request.args.to_dict()
    resid = args['reservationid']
    #Connect to db
    with requests.get(f'{API}/reservation/{resid}') as r:
        data = r.json()
        #Gets all reservation information
        HTMLOut = '<div class="card" style="width: 36rem;">'
        HTMLOut += f'<div class="card-header text-center">Reservation</div>'
        HTMLOut += f'<ul class="list-group list-group-flush">'

        res = data["reservations"][0]
        #sets eaier to read variables
        resid = res["ReservationID"]
        startdate = res["StartDate"]
        enddate = res["EndDate"]
        name = f'{res["FirstName"]} {res["LastName"]}'
        guestid = res["GuestID"]
        rooms = res["rooms"]



        #Generates HTML
        HTMLOut += '<li class="list-group-item"><ul style="list-style: none">'
        HTMLOut += f'<li><p><b>ReservationID:</b>{resid}</p></li>'
        HTMLOut += f'<li><p><b>Start Date:</b> {startdate}</p></li>'
        HTMLOut += f'<li><p><b>End Date:</b> {enddate}</p></li>'
        HTMLOut += f'<li><p><b>Rooms Booked:</b></p>'
        for room in rooms:
            HTMLOut += f'<div><a class="btn btn-outline-secondary" role="button" href="/rooms/search?roomnumber={room}">{room}</a></div>'

        HTMLOut += f'</li>'
        HTMLOut += f'<li><b>Guest:</b> <a class="btn btn-outline-secondary" role="button" href="/guest/search?guestid={guestid}">{name}</a></li>'
        HTMLOut += '</ul></li>'

        HTMLOut += f'</ul></div>'
        HTMLOut = Markup(HTMLOut)

        return render_template('index.html', content=HTMLOut)

#Here you can look at a guests reservations or a specific reservation
@app.route('/guest/reservation/search', methods=['GET'])
def get_guestreservation():
    #check if connection can be made

    if check_connection() == False:
        HTMLOut = '<div class="card" style="width: 40rem;">'
        HTMLOut += f'<div class="card-header text-center">Error: Could not connect to API</div>'
        HTMLOut += f'</div>'

        HTMLOut = Markup(HTMLOut)
        return render_template('index.html', content=HTMLOut)
    
    args = request.args.to_dict()
    guestid = args['guestid']
    with requests.get(f'{API}/reservation/') as r:
        data = r.json()
        data = data["reservations"]
        #Gsets vatriable to Guest Name

        HTMLOut = '<div class="card" style="width: 36rem;">'
        HTMLOut += f'<div class="card-header text-center">Reservation</div>'
        HTMLOut += f'<ul class="list-group list-group-flush">'

        for res in data:
            if res["GuestID"] == int(guestid):
        
                resid = res["ReservationID"]
                startdate = res["StartDate"]
                enddate = res["EndDate"]
                #gen HTML
                HTMLOut += f'<li class="list-group-item">'
                HTMLOut += f'<b>Reservation ID:</b> <a class="btn btn-outline-secondary" role="button" href="/reservation/search?reservationid={resid}">{resid}</a> '
                HTMLOut += f'<b>Start Date:</b> {startdate} '
                HTMLOut += f'<b>End Date:</b> {enddate}'
                HTMLOut += f'</li>'

    HTMLOut += f'</ul></div>'
    HTMLOut = Markup(HTMLOut)

    return render_template('index.html', content=HTMLOut)

#Route for guests
@app.route('/guest/')
def guests():
    #check if connection can be made

    if check_connection() == False:
        HTMLOut = '<div class="card" style="width: 40rem;">'
        HTMLOut += f'<div class="card-header text-center">Error: Could not connect to API</div>'
        HTMLOut += f'</div>'

        HTMLOut = Markup(HTMLOut)
        return render_template('index.html', content=HTMLOut)
    #Connects to DB
    with requests.get(f'{API}/guest/') as r:
        data = r.json()
        data = data["guests"]
        #Title
        HTMLOut = '<div class="card" style="width: 15rem;">'
        HTMLOut += f'<div class="card-header text-center">Guests</div>'
        HTMLOut += f'<ul class="list-group list-group-flush">'
        #For every guest, creates a hyperlink to their "OWN" page with information about each guest
        for guest in data:
            guestid = guest["GuestID"]
            name = f'{guest["FirstName"]} {guest["LastName"]}'
            HTMLOut += f'<li class="list-group-item"><a class="btn btn-outline-secondary" role="button" href="/guest/search?guestid={guestid}">{name}</a></li>'
        
        HTMLOut += f'</ul></div>'

        HTMLOut = Markup(HTMLOut)
        return render_template('index.html', content=HTMLOut)

#Connect city table by zip code!!
@app.route('/guest/search', methods=['GET'])
def get_guest():
    #check if connection can be made

    if check_connection() == False:
        HTMLOut = '<div class="card" style="width: 40rem;">'
        HTMLOut += f'<div class="card-header text-center">Error: Could not connect to API</div>'
        HTMLOut += f'</div>'

        HTMLOut = Markup(HTMLOut)
        return render_template('index.html', content=HTMLOut)
    
    #Gets arguments from URL
    args = request.args.to_dict()
    guestid = args['guestid']
    with requests.get(f'{API}/guest/{guestid}') as r:
        data = r.json()
        guest = data["guests"][0]
        #Output string
        HTMLOut = '<div class="card" style="width: 20rem;">'
        
        #variables from query
        name = f'{guest["FirstName"]} {guest["LastName"]}'
        address = f'{guest["Address"]}, {guest["City"]}, {guest["State"]}, {guest["ZipCode"]}'
        phone = guest["Phone"]
        #generating HTML
        HTMLOut += f'<div class="card-header text-center">{name}</div>'
        HTMLOut += f'<ul class="list-group list-group-flush">'
        HTMLOut += f'<li class="list-group-item"><p><b>Address: </b> {address}</p></li>'
        HTMLOut += f'<li class="list-group-item"><p><b>Phone:</b> {phone}</p></li>'
        HTMLOut += f'<li class="list-group-item"><a class="btn btn-outline-secondary" role="button" href="/guest/reservation/search?guestid={guestid}">Reservations</a></li>'
        HTMLOut += '</div>'
        
        HTMLOut = Markup(HTMLOut)

        return render_template('index.html', content=HTMLOut)

@app.route('/rooms')
def rooms():
    #check if connection can be made

    if check_connection() == False:
        HTMLOut = '<div class="card" style="width: 40rem;">'
        HTMLOut += f'<div class="card-header text-center">Error: Could not connect to API</div>'
        HTMLOut += f'</div>'

        HTMLOut = Markup(HTMLOut)
        return render_template('index.html', content=HTMLOut)
    
    #Connects to DB
    with requests.get(f'{API}/room/') as r:
        data = r.json()
        data = data["rooms"]
        HTMLOut = '<div class="card text-center" style="width: 30rem;">'
        HTMLOut += f'<div class="card-header">Rooms</div>'
        HTMLOut += f'<ul class="list-group list-group-flush">'
        #For every Room, creates a hyperlink to their "OWN" page with information about each Room
        for room in data:
            roomnum = room["RoomNumber"]
            roomtype = room["Type"]
            price = room["Price"]
            typeid = room["TypeID"]
            #html for the room information
            HTMLOut += f'<li class="list-group-item">'
            HTMLOut += f'<b>Room Number:</b> <a class="btn btn-outline-secondary" role="button" href="/rooms/search?roomnumber={roomnum}">{roomnum}</a> '
            HTMLOut += f'<b>Type:</b> <a class="btn btn-outline-secondary" role="button" href="/type/search?type={typeid}">{roomtype}</a> '
            HTMLOut += f'<b>Price: </b>${price}'
            HTMLOut += f'</li>'

        HTMLOut += f'</ul></div>'
        HTMLOut = Markup(HTMLOut)

        return render_template('index.html', content=HTMLOut)
    
@app.route('/rooms/search', methods=['GET'])
def get_room():
    #check if connection can be made

    if check_connection() == False:
        HTMLOut = '<div class="card" style="width: 40rem;">'
        HTMLOut += f'<div class="card-header text-center">Error: Could not connect to API</div>'
        HTMLOut += f'</div>'

        HTMLOut = Markup(HTMLOut)
        return render_template('index.html', content=HTMLOut)
    
    #Gets arguments from URL
    args = request.args.to_dict()
    roomnum = args['roomnumber']
    #Connects to DB
    with requests.get(f'{API}/room/{roomnum}') as r:
        data = r.json()

        room = data["rooms"][0]
        roomnum = room["RoomNumber"]
        roomtype = room["Type"]
        typeid = room["TypeID"]
        #Close to make new  query
        
        #Will Hold All Amenities
        #amenities = ''
        
        #for amen in cursor.fetchall():
        #    amenities += f'<p> {amen[0]} </p>'
        
        HTMLOut = '<div class="card" style="width: 18rem;">'
        HTMLOut += f'<div class="card-header text-center"><h5>{roomnum}</h5></div>'
        HTMLOut += f'<ul class="list-group list-group-flush">'
        HTMLOut += f'<li class="list-group-item">Room Is a: <a class="btn btn-outline-secondary" role="button" href="/type/search?type={typeid}">{roomtype}</a></li>'
        HTMLOut += f'<li class="list-group-item">Amenities Included in the Room:</li>'
        HTMLOut += f'</ul>'
        HTMLOut += '</div>'
        #HTMLOut += f'<div>{amenities}</div>'
        HTMLOut += f'</ul></div>'
        HTMLOut = Markup(HTMLOut)

        return render_template('index.html', content=HTMLOut)

#Room Types Page
@app.route('/type/search', methods=['GET'])
def get_type():
    #check if connection can be made

    if check_connection() == False:
        HTMLOut = '<div class="card" style="width: 40rem;">'
        HTMLOut += f'<div class="card-header text-center">Error: Could not connect to API</div>'
        HTMLOut += f'</div>'

        HTMLOut = Markup(HTMLOut)
        return render_template('index.html', content=HTMLOut)
    
    #Gets arguments from URL
    args = request.args.to_dict()
    typeid = args['type']

    with requests.get(f'{API}/type/{typeid}') as r:
        data = r.json()
        typeinfo = data["type"][0]
        #naming all the type information
        name = typeinfo["Name"]
        pricePerNight = typeinfo["Price"]
        priceExtra = typeinfo["PriceExtraPerson"]
        standOcc = typeinfo["StandardOccupancy"]
        maxOcc = typeinfo["MaxOccupancy"]
        #Output
        HTMLOut = '<div class="card" style="width: 18rem;">'
        HTMLOut += f'<div class="card-header text-center"><h5>{name}</h5></div>'
        HTMLOut += f'<ul class="list-group list-group-flush">'
        HTMLOut += f'<li class="list-group-item"><b>Price Per Night: </b>{pricePerNight} </li>'
        HTMLOut += f'<li class="list-group-item"><b>Price Per Extra Person: </b> {priceExtra} </li>'
        HTMLOut += f'<li class="list-group-item"><b>Standard Occupancy: </b> {standOcc} </li>'
        HTMLOut += f'<li class="list-group-item"><b>Maximum Occupancy</b> {maxOcc}</li>'


    HTMLOut = Markup(HTMLOut)

    return render_template('index.html', content=HTMLOut)

#Main page, will display guest, reservations ext, so you can slects based on table =
@app.route('/')
def index():
    #Here we are sayin that our HTMl is safe
    #HTMLOut = Markup('<h1>Hotel</h1><a class="btn btn-outline-secondary" role="button" href="/guest">Guests</a> <a class="btn btn-outline-secondary" role="button" href="/rooms">Rooms</a> <a class="btn btn-outline-secondary" role="button" href="/reservation">Reservations</a>')
    #Here we open out HTML file and place out HTML into our content tab

    HTMLOut = '<div class="card">'
    HTMLOut += '<div class="card-body">'
    HTMLOut += '<h5 class="card-title">Hotel Portal Home</h5>'
    HTMLOut += '<p class="card-text">Welcome To Your Portal, Please Navigate using the Navigation Bar!</p>'
    HTMLOut += '</div>'
    HTMLOut += '</div>'

    HTMLOut = Markup(HTMLOut)

    return render_template('index.html', content=HTMLOut)

if __name__ == "__main__":
    app.run(debug=True, port=5000)