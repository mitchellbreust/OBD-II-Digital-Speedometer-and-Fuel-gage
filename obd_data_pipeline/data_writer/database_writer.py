import psycopg2
import logging
from typing import Dict, Any

class DatabaseWriter:
    def __init__(self, dbname: str, user: str, userid: int) -> None:
        self.dbname = dbname
        self.user = user
        self.userid = userid

    def insert_new_data(self, timestamp, data: Dict[str, Any]) -> None:
        connection = None
        cursor = None
        try:
            connection = psycopg2.connect(dbname=self.dbname, user=self.user)
            cursor = connection.cursor()
            logging.info("Database connection established.")

            timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')

            # Check if the timestamp already exists in the database
            cursor.execute("""
                SELECT id FROM timestamps WHERE timestamp = %s;
            """, (timestamp_str,))
            result = cursor.fetchone()

            if result:
                timestamp_id = result[0]
            else:
                cursor.execute("""
                    INSERT INTO timestamps (timestamp) VALUES (%s) RETURNING id;
                """, (timestamp_str,))
                timestamp_id = cursor.fetchone()[0]

            # Insert data into the respective tables
            self._insert_fuel_level(cursor, timestamp_id, data.get('fuel_level'))
            self._insert_fuel_cons(cursor, timestamp_id, data.get('fuel_cons'))
            self._insert_rpm(cursor, timestamp_id, data.get('rpm'))
            self._insert_coolant(cursor, timestamp_id, data.get('coolant'))
            self._insert_intake_manifold(cursor, timestamp_id, data.get('intake_manifold'))
            self._insert_mass_air_flow(cursor, timestamp_id, data.get('mass_air_flow'))
            self._insert_oxygen(cursor, timestamp_id, data.get('oxygen'))
            self._insert_speed(cursor, timestamp_id, data.get('speed'))
            self._insert_throttle(cursor, timestamp_id, data.get('throttle'))
            self._insert_diagnostic_codes(cursor, timestamp_id, data.get('diagnostic_codes'))
            self._insert_voltage(cursor, timestamp_id, data.get('battery'))

            connection.commit()
            logging.info(f"Data committed to the database at {timestamp_str}.")

        except psycopg2.DatabaseError as e:
            logging.error(f"Database error occurred: {e}")
            if connection:
                connection.rollback()
            raise
        except Exception as e:
            logging.error(f"Failed to insert data: {e}")
            if connection:
                connection.rollback()
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
            logging.info("Database connection closed.")

    def _insert_fuel_level(self, cursor, timestamp_id, fuel_level):
        if fuel_level is not None:
            cursor.execute("""
                INSERT INTO Fuel_level (User_Id, fuel, timestamp_id)
                VALUES (%s, %s, %s);
            """, (self.userid, fuel_level, timestamp_id))

    def _insert_fuel_cons(self, cursor, timestamp_id, fuel_cons):
        if fuel_cons is not None:
            cursor.execute("""
                INSERT INTO Fuel_cons (User_Id, consumption, timestamp_id)
                VALUES (%s, %s, %s);
            """, (self.userid, fuel_cons, timestamp_id))

    def _insert_rpm(self, cursor, timestamp_id, rpm):
        if rpm is not None:
            cursor.execute("""
                INSERT INTO RPM (User_Id, amount, timestamp_id)
                VALUES (%s, %s, %s);
            """, (self.userid, rpm, timestamp_id))

    def _insert_coolant(self, cursor, timestamp_id, coolant):
        if coolant is not None:
            cursor.execute("""
                INSERT INTO Coolant (User_Id, temp, timestamp_id)
                VALUES (%s, %s, %s);
            """, (self.userid, coolant, timestamp_id))

    def _insert_intake_manifold(self, cursor, timestamp_id, intake_manifold):
        if intake_manifold is not None:
            cursor.execute("""
                INSERT INTO Intake_manifold (User_Id, level, timestamp_id)
                VALUES (%s, %s, %s);
            """, (self.userid, intake_manifold, timestamp_id))

    def _insert_mass_air_flow(self, cursor, timestamp_id, mass_air_flow):
        if mass_air_flow is not None:
            cursor.execute("""
                INSERT INTO Mass_air_flow (User_Id, air_flow, timestamp_id)
                VALUES (%s, %s, %s);
            """, (self.userid, mass_air_flow, timestamp_id))

    def _insert_oxygen(self, cursor, timestamp_id, oxygen):
        if oxygen is not None:
            cursor.execute("""
                INSERT INTO Oxygen (User_Id, oxygen_level, timestamp_id)
                VALUES (%s, %s, %s);
            """, (self.userid, oxygen, timestamp_id))

    def _insert_speed(self, cursor, timestamp_id, speed):
        if speed is not None:
            cursor.execute("""
                INSERT INTO Speed_kph (User_Id, speed, timestamp_id)
                VALUES (%s, %s, %s);
            """, (self.userid, speed, timestamp_id))

    def _insert_throttle(self, cursor, timestamp_id, throttle):
        if throttle is not None:
            cursor.execute("""
                INSERT INTO Throttle (User_Id, position, timestamp_id)
                VALUES (%s, %s, %s);
            """, (self.userid, throttle, timestamp_id))

    def _insert_diagnostic_codes(self, cursor, timestamp_id, diagnostic_codes):
        if diagnostic_codes:
            for code in diagnostic_codes:
                cursor.execute("""
                    INSERT INTO DC (User_Id, code, timestamp_id)
                    VALUES (%s, %s, %s);
                """, (self.userid, code, timestamp_id))

    def _insert_voltage(self, cursor, timestamp_id, voltage_value):
        if voltage_value is not None:
            cursor.execute("""
                INSERT INTO voltage (User_Id, volt, timestamp_id)
                VALUES (%s, %s, %s);
            """, (self.userid, voltage_value, timestamp_id))


