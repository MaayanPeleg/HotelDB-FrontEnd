#run "pip install mysql-connector-python flask markupsafe"
# run with "flask --app server run --debug"
from flask import Flask, request, render_template
import mysql.connector as mysql
import requests
from markupsafe import Markup

app = Flask(__name__)

API = 'http://localhost:8000'

@app.route('/reservation/')
def reservation():
    #Connect to db
    with requests.get(f'{API}/reservation/') as r:
        data = r.json()
        #OUtput
        HTMLOut = '<h1>Reservations</h1>'
        #For all reservations
        for res in data['reservations']:
            #sets variables to make code more understandable
            resid = res["ReservationID"]
            startdate = res["StartDate"]
            enddate = res["EndDate"]
            name = f'{res["FirstName"]} {res["LastName"]}'
            guestid = res["GuestID"]

            #Generates HTML
            HTMLOut += '<div><p>'
            HTMLOut += f'<b>ReservationID:</b> <a href="/reservation/search?reservationid={resid}">{resid}</a> '
            HTMLOut += f'<b>Start Date:</b> {startdate} '
            HTMLOut += f'<b>End Date:</b> {enddate} '
            HTMLOut += f'<b>Guest:</b> <a href="/guest/search?guestid={guestid}">{name}</a>'
            HTMLOut += '</p></div>'
        #displays HTML
        HTMLOut = Markup(HTMLOut)

        return render_template('index.html', content=HTMLOut)

@app.route('/reservation/search', methods=['GET'])
def get_reservation():
    args = request.args.to_dict()
    resid = args['reservationid']
    #Connect to db
    with requests.get(f'{API}/reservation/{resid}') as r:
        data = r.json()
        #Gets all reservation information
        HTMLOut = '<h1>Reservation</h1>'

        res = data["reservations"][0]
        #sets eaier to read variables
        resid = res["ReservationID"]
        startdate = res["StartDate"]
        enddate = res["EndDate"]
        name = f'{res["FirstName"]} {res["LastName"]}'
        guestid = res["GuestID"]
        rooms = res["rooms"]



        #Generates HTML
        HTMLOut += '<div>'
        HTMLOut += f'<div><p><b>ReservationID:</b>{resid}</p></div>'
        HTMLOut += f'<div><p><b>Start Date:</b> {startdate}</p></div>'
        HTMLOut += f'<div><p><b>End Date:</b> {enddate}</p></div>'
        HTMLOut += f'<div><p><b>Rooms Booked:</b></p>'
        for room in rooms:
            HTMLOut += f'<div><a href="/rooms/search?roomnumber={room}">{room}</a></div>'

        HTMLOut += f'</div>'
        HTMLOut += f'<div><b>Guest:</b> <a href="/guest/search?guestid={guestid}">{name}</a></div>'
        HTMLOut += '</div>'

        HTMLOut = Markup(HTMLOut)

        return render_template('index.html', content=HTMLOut)

#Here you can look at a guests reservations or a specific reservation
@app.route('/guest/reservation/search', methods=['GET'])
def get_guestreservation():
    args = request.args.to_dict()
    guestid = args['guestid']
    with requests.get(f'{API}/reservation/') as r:
        data = r.json()
        data = data["reservations"]
        #Gsets vatriable to Guest Name

        HTMLOut = '<h1>Reservation</h1>'

        for res in data:
            if res["GuestID"] == int(guestid):
        
                resid = res["ReservationID"]
                startdate = res["StartDate"]
                enddate = res["EndDate"]
                #gen HTML
                HTMLOut += f'<p>'
                HTMLOut += f'<b>Reservation ID:</b> <a href="/reservation/search?reservationid={resid}">{resid}</a> '
                HTMLOut += f'<b>Start Date:</b> {startdate} '
                HTMLOut += f'<b>End Date:</b> {enddate}'
                HTMLOut += f'</p>'
    HTMLOut = Markup(HTMLOut)

    return render_template('index.html', content=HTMLOut)

#Route for guests
@app.route('/guest/')
def guests():
    #Connects to DB
    with requests.get(f'{API}/guest/') as r:
        data = r.json()
        data = data["guests"]
        #Title
        HTMLOut = '<h1>Guests</h1>'
        #For every guest, creates a hyperlink to their "OWN" page with information about each guest
        for guest in data:
            guestid = guest["GuestID"]
            name = f'{guest["FirstName"]} {guest["LastName"]}'
            HTMLOut += f'<div><a href="/guest/search?guestid={guestid}">{name}</a></div>'
        
        HTMLOut = Markup(HTMLOut)
        return render_template('index.html', content=HTMLOut)

#Connect city table by zip code!!
@app.route('/guest/search', methods=['GET'])
def get_guest():
    args = request.args.to_dict()
    guestid = args['guestid']
    with requests.get(f'{API}/guest/{guestid}') as r:
        data = r.json()
        guest = data["guests"][0]
        #Output string
        HTMLOut = '<h1>Guest</h1>'
        #variables from query
        name = f'{guest["FirstName"]} {guest["LastName"]}'
        address = f'{guest["Address"]}, {guest["City"]}, {guest["State"]}, {guest["ZipCode"]}'
        phone = guest["Phone"]
        #generating HTML
        HTMLOut += '<div>'
        HTMLOut += f'<div><p><b>Name:</b> {name}</p></div>'
        HTMLOut += f'<div><p><b>Address: </b> {address}</p></div>'
        HTMLOut += f'<div><p><b>Phone:</b> {phone}</p></div>'
        HTMLOut += f'<div><a href="/guest/reservation/search?guestid={guestid}">Reservations</a></div>'
        HTMLOut += '</div>'
        
        HTMLOut = Markup(HTMLOut)

        return render_template('index.html', content=HTMLOut)

@app.route('/rooms')
def rooms():
    #Connects to DB
    with requests.get(f'{API}/room/') as r:
        data = r.json()
        data = data["rooms"]
        HTMLOut = '<h1>Rooms</h1>'
        #For every Room, creates a hyperlink to their "OWN" page with information about each Room
        for room in data:
            roomnum = room["RoomNumber"]
            roomtype = room["Type"]
            price = room["Price"]
            typeid = room["TypeID"]
            #html for the room information
            HTMLOut += f'<div><p>'
            HTMLOut += f'<b>Room Number:</b> <a href="/rooms/search?roomnumber={roomnum}">{roomnum}</a> '
            HTMLOut += f'<b>Type:</b> <a href="/type/search?type={typeid}">{roomtype}</a> '
            HTMLOut += f'<b>Price: </b>${price}'
            HTMLOut += f'</p></div>'

        HTMLOut = Markup(HTMLOut)

        return render_template('index.html', content=HTMLOut)
    
@app.route('/rooms/search', methods=['GET'])
def get_room():
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
        
        HTMLOut = f'<h1>{roomnum}</h1>'
        HTMLOut += f'<p><b>Room Is a: </b><a href="/type/search?type={typeid}">{roomtype}</a></p><p><b>Amenities Included in the Room:</b> </p>'
        #HTMLOut += f'<div>{amenities}</div>'
        HTMLOut = Markup(HTMLOut)

        return render_template('index.html', content=HTMLOut)

#Room Types Page
@app.route('/type/search', methods=['GET'])
def get_type():
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
        HTMLOut = f'<h1>{name}</h1>'
        HTMLOut += f'<div><b>Price Per Night: </b>{pricePerNight} </div>'
        HTMLOut += f'<div><b>Price Per Extra Person: </b> {priceExtra} </div>'
        HTMLOut += f'<div><b>Standard Occupancy: </b> {standOcc} </div>'
        HTMLOut += f'<div><b>Maximum Occupancy</b> {maxOcc}</div>'

    HTMLOut = Markup(HTMLOut)

    return render_template('index.html', content=HTMLOut)

#Main page, will display guest, reservations ext, so you can slects based on table =
@app.route('/')
def index():
    #Here we are sayin that our HTMl is safe
    #HTMLOut = Markup('<h1>Hotel</h1><a href="/guest">Guests</a> <a href="/rooms">Rooms</a> <a href="/reservation">Reservations</a>')
    #Here we open out HTML file and place out HTML into our content tab
    return render_template('index.html', content='')

'''if __name__ == "__main__":
    app.run()'''