from flask import Flask
from flask import Response
from data_access import DataAccess
from flask import abort, redirect, url_for
import msgpack

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

        # Serialize the numpy arrays with MessagePack
        packed_data = msgpack.packb({'timestamp': timestamp, 'data': data}, use_bin_type=True)

        # Send the serialized data as a response
        return Response(packed_data, content_type='application/x-msgpack')
        
    
    except:
        pass
