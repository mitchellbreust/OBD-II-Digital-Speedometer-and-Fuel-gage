import msgpack
import requests
import numpy as np
import pandas as pd
import sys

def get_data(user_id, interval, data_type):
    """
    General function to fetch speed data for a given user and interval.
    Args:
        user_id (int): The ID of the user.
        interval (str): The time interval (e.g., '5s', '30s', '2min', '30min', '2hours').

    Returns:
        pd.DataFrame: A DataFrame with the timestamps and speed data.
    """

    allowed_data = ['speed', 'fuel_level', 'fuel_consumption', 'maf', 'oxygen', 'throttle', 'coolant', 'intake_manifold', 'rpm']
    if data_type not in allowed_data:
        print(f"data type of {data_type} is not supported", file=sys.stderr)
        return None

    try:
        start_of_url = "http://127.0.0.1:5000"
        # Construct the URL with the provided user ID and interval
        res = requests.get(f"{start_of_url}/{data_type}/{user_id}/{interval}")
        
        if res.status_code != 200:
            print(f"Request failed with status code: {res.status_code} - {res.text}", file=sys.stderr)
            return None

        # Unpack the MessagePack data
        res_data = msgpack.unpackb(res.content)
        
        
        # Convert timestamps and speed data to NumPy arrays
        time_stamps = np.array(res_data.get('timestamp'))
        data = np.array(res_data.get('data'))

        print(time_stamps)
        print(data)



        return pd.DataFrame({
            'timestamp': pd.to_datetime(time_stamps),
            'data': data
        })

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}", file=sys.stderr)
        return None
