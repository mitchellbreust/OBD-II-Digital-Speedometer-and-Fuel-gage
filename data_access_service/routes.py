from flask import Flask
from data_access import DataAccess
from flask import abort, redirect, url_for

app = Flask(__name__)

def valid_interval(interval):
    return interval in ['5s', '30s', '2min', '30min', '2hours']

@app.get("/speed/<int:user_id>/<string:interval>")
def get_users_speed(user_id, interval):

    if not valid_interval(interval):
        abort(400, description='invalid interval')

    try:
        data_access = DataAccess(user_id)

        if not data_access._is_valid_user_id(user_id):
            abort(400, description=f'invalid user id: {user_id}')

        timestamp, data = data_access.get_speed()
        
    
    except:
        pass
