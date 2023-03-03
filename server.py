#run "pip install mysql-connector-python flask markupsafe"
# run with "flask --app server run --debug"
from flask import Flask, request, render_template
import mysql.connector as mysql
from markupsafe import Markup

app = Flask(__name__)

#The information to connect to the database
config = {
    'user': 'root',
    'password': 'ABC123',
    'host': 'localhost',
    'database': 'Hotel'
}

@app.route('/reservation')
def reservation():
    #Connect to db
    with mysql.connect(**config) as conn:
        cursor = conn.cursor()
        #Gets all reservations and their geust
        cursor.execute('''SELECT res.ReservationID, res.StartDate, res.EndDate, g.FirstName, g.LastName, g.GuestID
        FROM Reservation res
        JOIN Guest g ON g.GuestID = res.GuestID
        ORDER BY res.ReservationID;''')
        #OUtput
        HTMLOut = '<h1>Reservations</h1>'
        #For all reservations
        for res in cursor.fetchall():
            #sets variables to make code more understandable
            resid = res[0]
            startdate = res[1]
            enddate = res[2]
            name = f'{res[3]} {res[4]}'
            guestid = res[5]

            #Generates HTML
            HTMLOut += '<div><p>'
            HTMLOut += f'<b>ReservationID:</b> <a href="reservation/search?reservationid={resid}">{resid}</a> '
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
    with mysql.connect(**config) as conn:
        cursor = conn.cursor()
        #Gets all reservation information
        cursor.execute('''SELECT res.ReservationID, res.StartDate, res.EndDate, g.FirstName, g.LastName, g.GuestID
        FROM Reservation res
        JOIN Guest g ON g.GuestID = res.GuestID
        JOIN RoomReservation rr ON rr.ReservationID = res.ReservationID
        WHERE res.ReservationID = %s;''',(resid,))

        HTMLOut = '<h1>Reservation</h1>'

        res = cursor.fetchall()[0]
        #sets eaier to read variables
        resid = res[0]
        startdate = res[1]
        enddate = res[2]
        name = f'{res[3]} {res[4]}'
        guestid = res[5]

        cursor.close()
        cursor = conn.cursor()
        cursor.execute('''SELECT RoomNumber FROM RoomReservation WHERE ReservationID = %s''', (resid,))
        rooms = cursor.fetchall()

        #Generates HTML
        HTMLOut += '<div>'
        HTMLOut += f'<div><p><b>ReservationID:</b>{resid}</p></div>'
        HTMLOut += f'<div><p><b>Start Date:</b> {startdate}</p></div>'
        HTMLOut += f'<div><p><b>End Date:</b> {enddate}</p></div>'
        HTMLOut += f'<div><p><b>Rooms Booked:</b></p>'
        for room in rooms:
            roomnum = room[0]
            HTMLOut += f'<div><a href="/rooms/search?roomnumber={roomnum}">{roomnum}</a></div>'

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
    with mysql.connect(**config) as conn:
        cursor = conn.cursor()
        #selects geust neam
        cursor.execute('SELECT FirstName, LastName FROM Guest WHERE GuestID = %s',(guestid,))
        guest = cursor.fetchall()[0]
        #Gsets vatriable to Guest Name
        name = f'{guest[0]} {guest[1]}'
        cursor.close()

        cursor = conn.cursor()
        #Reservation infor a a given guest
        cursor.execute('SELECT ReservationID, StartDate, EndDate FROM Reservation WHERE GuestID = %s;', (guestid,))
        #ADD GUEST NAME
        HTMLOut = '<h1>Reservation</h1>'
        HTMLOut += f'<h2>{name}</h2>'
        for res in cursor.fetchall():
            resid = res[0]
            startdate = res[1]
            enddate = res[2]
            #gen HTML
            HTMLOut += f'<p>'
            HTMLOut += f'<b>Reservation ID:</b> <a href="/reservation/search?reservationid={resid}">{resid}</a> '
            HTMLOut += f'<b>Start Date:</b> {startdate} '
            HTMLOut += f'<b>End Date:</b> {enddate}'
            HTMLOut += f'</p>'
    HTMLOut = Markup(HTMLOut)

    return render_template('index.html', content=HTMLOut)

#Route for guests
@app.route('/guest')
def guests():
    #Connects to DB
    with mysql.connect(**config) as conn:
        cursor = conn.cursor()
        #Executes Select Query to get all guests
        cursor.execute('SELECT GuestID, FirstName, LastName FROM Guest;')
        #Title
        HTMLOut = '<h1>Guests</h1>'
        #For every guest, creates a hyperlink to their "OWN" page with information about each guest
        for guest in cursor.fetchall():
            guestid = guest[0]
            gfirstname = guest[1]
            glastname = guest[2]
            HTMLOut += f'<div><a href="/guest/search?guestid={guestid}">{gfirstname} {glastname}</a></div>'
        
        HTMLOut = Markup(HTMLOut)
        return render_template('index.html', content=HTMLOut)

#Connect city table by zip code!!
@app.route('/guest/search', methods=['GET'])
def get_guest():
    args = request.args.to_dict()
    guestid = args['guestid']
    with mysql.connect(**config) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT g.FirstName, g.LastName, g.Address, c.City, c.State, c.Zipcode, g.Phone 
        FROM Guest g
        JOIN City c ON c.Zipcode = g.Zipcode
        WHERE GuestID = %s;''', (guestid,))
        guest = cursor.fetchall()[0]
        #Output string
        HTMLOut = '<h1>Guest</h1>'
        #variables from query
        name = f'{guest[0]} {guest[1]}'
        address = f'{guest[2]}, {guest[3]}, {guest[4]}, {guest[5]}'
        phone = guest[6]
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
    with mysql.connect(**config) as conn:
        cursor = conn.cursor()
        #Executes Select Query to get all rooms and types
        cursor.execute('SELECT r.RoomNumber, t.Name, g.PriceA FROM Room r JOIN Type t ON r.TypeID = t.TypeID JOIN get_price g ON g.RoomNumber = r.RoomNumber;')
        #Title
        HTMLOut = '<h1>Rooms</h1>'
        #For every Room, creates a hyperlink to their "OWN" page with information about each Room
        for room in cursor.fetchall():
            roomnum = room[0]
            roomtype = room[1]
            price = room[2]
            #html for the room information
            HTMLOut += f'<div><p>'
            HTMLOut += f'<b>Room Number:</b> <a href="/rooms/search?roomnumber={roomnum}">{roomnum}</a> '
            HTMLOut += f'<b>Type:</b> <a href="/type/search?type={roomtype}">{roomtype}</a> '
            HTMLOut += f'<b>Price: </b>${price}'
            HTMLOut += f'</p></div>'

        HTMLOut = Markup(HTMLOut)

        return render_template('index.html', content=HTMLOut)
    
@app.route('/rooms/search', methods=['GET'])
def get_room():
    args = request.args.to_dict()
    roomnum = args['roomnumber']
    #Connects to DB
    with mysql.connect(**config) as conn:
        cursor = conn.cursor()
        #Get Room Type
        cursor.execute('SELECT t.Name FROM Room r JOIN Type t ON r.TypeID = t.TypeID WHERE r.RoomNumber = %s;', (roomnum,))
        typename = cursor.fetchall()[0][0]
        #Close to make new  query
        cursor.close()

        cursor = conn.cursor()
        #Executes Select Query to get room information
        cursor.execute('''SELECT a.Name 
        FROM Amenities a 
        JOIN RoomAmenities ra ON ra.AmenitiesID = a.AmenitiesID 
        WHERE ra.RoomNumber = %s;''', (roomnum,))
        #Will Hold All Amenities
        amenities = ''
        
        for amen in cursor.fetchall():
            amenities += f'<p> {amen[0]} </p>'
        
        HTMLOut = f'<h1>{roomnum}</h1>'
        HTMLOut += f'<p><b>Room Is a: </b><a href="/type/search?type={typename}">{typename}</a></p><p><b>Amenities Included in the Room:</b> </p>'
        HTMLOut += f'<div>{amenities}</div>'
        HTMLOut = Markup(HTMLOut)

        return render_template('index.html', content=HTMLOut)

#Room Types Page
@app.route('/type/search', methods=['GET'])
def get_type():
    args = request.args.to_dict()
    typename = args['type']
    with mysql.connect(**config) as conn:
        cursor = conn.cursor()
        #Get Type information
        cursor.execute('SELECT Price, PriceExtraPerson, StandardOccupancy, MaxOccupancy FROM Type WHERE Name = %s;', (typename,))
        typeinfo = cursor.fetchall()[0]
        #naming all the type information
        pricePerNight = typeinfo[0]
        priceExtra = typeinfo[1]
        standOcc = typeinfo[2]
        maxOcc = typeinfo[3]
        #Output
        HTMLOut = f'<h1>{typename}</h1>'
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