from flask import Flask, request, jsonify, make_response, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# from marshmallow_sqlalchemy import ModelSchema
import os
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from datetime import datetime

import pymysql

import requests

# for websockets
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)

# application = app # our hosting requires application in passenger_wsgi
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db1.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/smart_parking'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# for websockets
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
# logger=True, engineio_logger=True

# Init db
db = SQLAlchemy(app)

# init ma
ma = Marshmallow(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True, index = True, unique = True)
    park_no = db.Column(db.String(50))
    status = db.Column(db.String(50))
    reservation = db.Column(db.String(50))
    res_time = db.Column(db.String(50))
    # name = db.Column(db.String(50))
    # reg_no = db.Column(db.String(50))
    # phone = db.Column(db.String(100))
    

    def __init__(self, park_no, status, reservation, res_time):
        self.park_no = park_no
        self.status = status
        self.reservation = reservation
        self.res_time = res_time
        
class UserSchema(ma.Schema):
    class Meta:
        # model = Users
        fields = ('id','park_no', 'status', 'reservation', 'res_time')
        
        
# init schema

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/parkingStatus', methods=['GET'])

def get_Allparking():
    all_parking = Users.query.all()
    result = users_schema.dump(all_parking)
    print('im printed')

    now = datetime.now().time()
    rightNow = (now.hour*3600)+(now.minute*60)+now.second
    print(rightNow)

    parkA1 = Users.query.get(1)
    park1 = user_schema.dump(parkA1)
    print(park1['res_time'])

    
    
    

    parkA2 = Users.query.get(2)
    park2 = user_schema.dump(parkA2)
    print(park2['res_time'])

    parkA3 = Users.query.get(3)
    park3 = user_schema.dump(parkA3)
    print(park3['res_time'])

    if (rightNow-park1['res_time'])>10:
        parkA1.reservation = 0
        db.session.commit()
    
    if (rightNow-park2['res_time'])>10:
        parkA2.reservation = 0
        db.session.commit()
    
    if (rightNow-park3['res_time'])>10:
        parkA3.reservation = 0
        db.session.commit()

    return jsonify({"result":result,
                    "code": 200})

@socketio.on('myevent', namespace='/')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    print('lola')

@socketio.on('myevent2', namespace='/test')
def handle_my_custom_event2(json):
    print('received json: ' + str(json))
    print('lola')

@app.route('/test1', methods=['GET'])
def lol():
    print("im herer")

# app.config['SECRET_KEY'] = APP_SECRET_KEY
# jwt = JWTManager(app)
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
# # app.config['transports'] = 'websocket'
# socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

@app.route('/some/<id>', methods=['PUT'])
def some_function(id):
    try:
        home = Users.query.get(id)

        reservation = request.json['reservation']

        time = datetime.now().time()

        home.reservation = reservation
        home.res_time = time

        db.session.commit()

        # socketio.emit('some', {'data': 42}, namespace='/chat')

        return jsonify({"result":"success",
                        "code": 200})

    except Exception as e:
        print(str(e))
        return jsonify({'error' : str(e),
                        "code": 4000})  

@app.route('/irSensor/<id>', methods=['PUT'])
def sensor_function(id):
    try:
        home = Users.query.get(id)

        # reservation = request.json['reservation']

        home.status = 1
        home.reservation = 0
        print(id)

        db.session.commit()

        # socketio.emit('some', {'data': 42}, namespace='/chat')

        return jsonify({"result":"success",
                        "code": 200})

    except Exception as e:
        print(str(e))
        return jsonify({'error' : str(e),
                        "code": 4000})  
    

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app, debug=True)
    # app.run(debug=True,host='0.0.0.0')