import psycopg2
import logging
import numpy as np
import pandas as pd
from datetime import timedelta

class DataAccess:
    def __init__(self, user_id) -> None:
        self.connection = None
        self.cur = None
        self.user_id = user_id

        try:
            self.connection = psycopg2.connect(dbname='car_data', user='mitchellbreust')
            self.cur = self.connection.cursor()
            logging.info("Database connection established.")
        except psycopg2.DatabaseError as e:
            logging.error(f"Database connection error occurred: {e}")
            if self.connection:
                self.connection.rollback()
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise

    def close_data_access(self):
        if self.cur:
            try:
                self.cur.close()
            except psycopg2.Error as e:
                logging.error(f"Error closing cursor: {e}")
            finally:
                self.cur = None

        if self.connection:
            try:
                self.connection.close()
                logging.info("Database connection closed.")
            except psycopg2.Error as e:
                logging.error(f"Error closing connection: {e}")
            finally:
                self.connection = None

    def get_speed(self, data_interval):
        return self._execute_query("SELECT * FROM UserSpeed WHERE User_Id = %s", (self.user_id,), data_interval)

    def get_fuel_level(self, data_interval):
        return self._execute_query("SELECT * FROM UserFuelLevel WHERE User_Id = %s", (self.user_id,), data_interval)

    def get_fuel_cons(self, data_interval):
        return self._execute_query("SELECT * FROM UserFuelConsumption WHERE User_Id = %s", (self.user_id,), data_interval)

    def get_maf(self, data_interval):
        return self._execute_query("SELECT * FROM UserMassAirFlow WHERE User_Id = %s", (self.user_id,), data_interval)

    def get_oxygen(self, data_interval):
        return self._execute_query("SELECT * FROM UserOxygenLevel WHERE User_Id = %s", (self.user_id,), data_interval)

    def get_throttle(self, data_interval):
        return self._execute_query("SELECT * FROM UserThrottlePosition WHERE User_Id = %s", (self.user_id,), data_interval)

    def get_coolant(self, data_interval):
        return self._execute_query("SELECT * FROM UserCoolantTemperature WHERE User_Id = %s", (self.user_id,), data_interval)

    def get_intake_manifold(self, data_interval):
        return self._execute_query("SELECT * FROM UserIntakeManifoldLevel WHERE User_Id = %s", (self.user_id,), data_interval)

    def get_rpm(self, data_interval):
        return self._execute_query("SELECT * FROM UserRPM WHERE User_Id = %s", (self.user_id,), data_interval)

    def _execute_query(self, query, params, interval):
        if not self.cur:
            logging.error("Cursor is not initialized.")
            return None, None

        try:
            self.cur.execute(query, params)
            result = self.cur.fetchall()

            # Unpack the result into three separate lists
            user_ids, timestamps, data = zip(*result)

            # Convert timestamps and data to NumPy arrays
            timestamps = np.array(timestamps)
            data = np.array(data)

            # Convert timestamps to a Pandas datetime index
            timestamps = pd.to_datetime(timestamps)

            # Determine the resample interval

            # Create a DataFrame and resample the data
            df = pd.DataFrame({'timestamp': timestamps, 'data': data})
            df.set_index('timestamp', inplace=True)
            df_resampled = df.resample(interval).mean().dropna()

            # Get the resampled timestamps and data
            timestamps_resampled = df_resampled.index.to_numpy()
            data_resampled = df_resampled['data'].to_numpy()

            return timestamps_resampled, data_resampled
        except psycopg2.DatabaseError as e:
            logging.error(f"Database error during query execution: {e}")
            if self.connection:
                self.connection.rollback()
            return None, None
        except Exception as e:
            logging.error(f"Unexpected error during query execution: {e}")
            return None, None