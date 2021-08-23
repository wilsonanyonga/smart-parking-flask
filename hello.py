from flask import Flask, request, jsonify, make_response, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# from marshmallow_sqlalchemy import ModelSchema
import os
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

import pymysql

import requests

app = Flask(__name__)

# application = app # our hosting requires application in passenger_wsgi
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db1.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/smart_parking'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


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

@app.route('/api/parkingStatus', methods=['GET'])

def get_Allparking():
    all_parking = Users.query.all()
    result = users_schema.dump(all_parking)
    return jsonify({"result":result,
                    "code": 200})

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(debug=True)