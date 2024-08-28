import psycopg2
import logging
import numpy as np

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

    def _execute_query(self, query, params):
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

            return timestamps, data
        except psycopg2.DatabaseError as e:
            logging.error(f"Database error during query execution: {e}")
            if self.connection:
                self.connection.rollback()
            return None, None
        except Exception as e:
            logging.error(f"Unexpected error during query execution: {e}")
            return None, None

    def get_speed(self):
        return self._execute_query("SELECT * FROM UserSpeed WHERE User_Id = %s", (self.user_id,))

    def get_fuel_level(self):
        return self._execute_query("SELECT * FROM UserFuelLevel WHERE User_Id = %s", (self.user_id,))

    def get_fuel_cons(self):
        return self._execute_query("SELECT * FROM UserFuelConsumption WHERE User_Id = %s", (self.user_id,))

    def get_maf(self):
        return self._execute_query("SELECT * FROM UserMassAirFlow WHERE User_Id = %s", (self.user_id,))

    def get_oxygen(self):
        return self._execute_query("SELECT * FROM UserOxygenLevel WHERE User_Id = %s", (self.user_id,))

    def get_throttle(self):
        return self._execute_query("SELECT * FROM UserThrottlePosition WHERE User_Id = %s", (self.user_id,))

    def get_coolant(self):
        return self._execute_query("SELECT * FROM UserCoolantTemperature WHERE User_Id = %s", (self.user_id,))

    def get_intake_manifold(self):
        return self._execute_query("SELECT * FROM UserIntakeManifoldLevel WHERE User_Id = %s", (self.user_id,))

    def get_rpm(self):
        return self._execute_query("SELECT * FROM UserRPM WHERE User_Id = %s", (self.user_id,))