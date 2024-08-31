from flask import Flask
from flask import Response
from data_access import DataAccess
from flask import abort
import numpy as np
import msgpack
import logging

app = Flask(__name__)

def valid_interval(interval):
    return interval in ['5s', '30s', '2min', '30min', '2hours']

def make_response(timestamp, data):
    # Convert NumPy arrays to lists for serialization
    timestamp_list = timestamp.tolist() if isinstance(timestamp, np.ndarray) else timestamp
    data_list = data.tolist() if isinstance(data, np.ndarray) else data

    # Pack the data using msgpack
    packed_data = msgpack.packb({'timestamp': timestamp_list, 'data': data_list}, use_bin_type=True)
    return Response(packed_data, content_type='application/x-msgpack')

@app.get("/speed/<int:user_id>/<string:interval>")
def get_users_speed(user_id, interval):
    if not valid_interval(interval):
        abort(400, description='invalid interval')

    data_access = None
    try:
        data_access = DataAccess(user_id)

        if not data_access._is_valid_user_id(user_id):
            abort(400, description=f'invalid user id: {user_id}')

        timestamp, data = data_access.get_speed(interval)
        return make_response(timestamp, data)
    except Exception as e:
        logging.error(f"Error while processing request: {e}")
        abort(500, description='Internal server error')
    finally:
        if data_access:
            data_access.close_data_access()

@app.get("/fuel_level/<int:user_id>/<string:interval>")
def get_users_fuel_level(user_id, interval):
    if not valid_interval(interval):
        abort(400, description='Invalid interval')

    data_access = None
    try:
        data_access = DataAccess(user_id)

        if not data_access._is_valid_user_id(user_id):
            abort(400, description=f'Invalid user id: {user_id}')

        timestamp, data = data_access.get_fuel_level(interval)
        return make_response(timestamp, data)
    except Exception as e:
        logging.error(f"Error while processing request: {e}")
        abort(500, description='Internal server error')
    finally:
        if data_access:
            data_access.close_data_access()

@app.get("/fuel_consumption/<int:user_id>/<string:interval>")
def get_users_fuel_consumption(user_id, interval):
    if not valid_interval(interval):
        abort(400, description='Invalid interval')

    data_access = None
    try:
        data_access = DataAccess(user_id)

        if not data_access._is_valid_user_id(user_id):
            abort(400, description=f'Invalid user id: {user_id}')

        timestamp, data = data_access.get_fuel_cons(interval)
        return make_response(timestamp, data)
    except Exception as e:
        logging.error(f"Error while processing request: {e}")
        abort(500, description='Internal server error')
    finally:
        if data_access:
            data_access.close_data_access()

@app.get("/maf/<int:user_id>/<string:interval>")
def get_users_maf(user_id, interval):
    if not valid_interval(interval):
        abort(400, description='Invalid interval')

    data_access = None
    try:
        data_access = DataAccess(user_id)

        if not data_access._is_valid_user_id(user_id):
            abort(400, description=f'Invalid user id: {user_id}')

        timestamp, data = data_access.get_maf(interval)
        return make_response(timestamp, data)
    except Exception as e:
        logging.error(f"Error while processing request: {e}")
        abort(500, description='Internal server error')
    finally:
        if data_access:
            data_access.close_data_access()

@app.get("/oxygen/<int:user_id>/<string:interval>")
def get_users_oxygen(user_id, interval):
    if not valid_interval(interval):
        abort(400, description='Invalid interval')

    data_access = None
    try:
        data_access = DataAccess(user_id)

        if not data_access._is_valid_user_id(user_id):
            abort(400, description=f'Invalid user id: {user_id}')

        timestamp, data = data_access.get_oxygen(interval)
        return make_response(timestamp, data)
    except Exception as e:
        logging.error(f"Error while processing request: {e}")
        abort(500, description='Internal server error')
    finally:
        if data_access:
            data_access.close_data_access()

@app.get("/throttle/<int:user_id>/<string:interval>")
def get_users_throttle(user_id, interval):
    if not valid_interval(interval):
        abort(400, description='Invalid interval')

    data_access = None
    try:
        data_access = DataAccess(user_id)

        if not data_access._is_valid_user_id(user_id):
            abort(400, description=f'Invalid user id: {user_id}')

        timestamp, data = data_access.get_throttle(interval)
        return make_response(timestamp, data)
    except Exception as e:
        logging.error(f"Error while processing request: {e}")
        abort(500, description='Internal server error')
    finally:
        if data_access:
            data_access.close_data_access()

@app.get("/coolant/<int:user_id>/<string:interval>")
def get_users_coolant(user_id, interval):
    if not valid_interval(interval):
        abort(400, description='Invalid interval')

    data_access = None
    try:
        data_access = DataAccess(user_id)

        if not data_access._is_valid_user_id(user_id):
            abort(400, description=f'Invalid user id: {user_id}')

        timestamp, data = data_access.get_coolant(interval)
        return make_response(timestamp, data)
    except Exception as e:
        logging.error(f"Error while processing request: {e}")
        abort(500, description='Internal server error')
    finally:
        if data_access:
            data_access.close_data_access()

@app.get("/intake_manifold/<int:user_id>/<string:interval>")
def get_users_intake_manifold(user_id, interval):
    if not valid_interval(interval):
        abort(400, description='Invalid interval')

    data_access = None
    try:
        data_access = DataAccess(user_id)

        if not data_access._is_valid_user_id(user_id):
            abort(400, description=f'Invalid user id: {user_id}')

        timestamp, data = data_access.get_intake_manifold(interval)
        return make_response(timestamp, data)
    except Exception as e:
        logging.error(f"Error while processing request: {e}")
        abort(500, description='Internal server error')
    finally:
        if data_access:
            data_access.close_data_access()

@app.get("/rpm/<int:user_id>/<string:interval>")
def get_users_rpm(user_id, interval):
    if not valid_interval(interval):
        abort(400, description='Invalid interval')

    data_access = None
    try:
        data_access = DataAccess(user_id)

        if not data_access._is_valid_user_id(user_id):
            abort(400, description=f'Invalid user id: {user_id}')

        timestamp, data = data_access.get_rpm(interval)
        return make_response(timestamp, data)
    except Exception as e:
        logging.error(f"Error while processing request: {e}")
        abort(500, description='Internal server error')
    finally:
        if data_access:
            data_access.close_data_access()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
