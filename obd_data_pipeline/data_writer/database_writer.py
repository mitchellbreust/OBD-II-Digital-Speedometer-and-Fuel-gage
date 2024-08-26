import psycopg2
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseWriter:
    def __init__(self, dbname: str, user: str, password: str, userid: int) -> None:
        try:
            self.connection = psycopg2.connect(dbname=dbname, user=user, password=password)
            self.cursor = self.connection.cursor()
            self.userid = userid
            logging.info("Database connection established.")
        except psycopg2.DatabaseError as e:
            logging.error(f"Failed to connect to the database: {e}")
            raise

    def insert_new_data(self, timestamp, data: Dict[str, Any]) -> None:
        try:
            timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')

            # Check if the timestamp already exists in the database
            self.cursor.execute("""
                SELECT id FROM timestamps WHERE timestamp = %s;
            """, (timestamp_str,))
            result = self.cursor.fetchone()

            if result:
                timestamp_id = result[0]
            else:
                self.cursor.execute("""
                    INSERT INTO timestamps (timestamp) VALUES (%s) RETURNING id;
                """, (timestamp_str,))
                timestamp_id = self.cursor.fetchone()[0]

            # Insert data into the respective tables
            self._insert_fuel_level(timestamp_id, data.get('fuel_level'))
            self._insert_fuel_cons(timestamp_id, data.get('fuel_cons'))
            self._insert_rpm(timestamp_id, data.get('rpm'))
            self._insert_coolant(timestamp_id, data.get('coolant'))
            self._insert_intake_manifold(timestamp_id, data.get('intake_manifold'))
            self._insert_mass_air_flow(timestamp_id, data.get('mass_air_flow'))
            self._insert_oxygen(timestamp_id, data.get('oxygen'))
            self._insert_speed(timestamp_id, data.get('speed'))
            self._insert_throttle(timestamp_id, data.get('throttle'))
            # Additional insertions for battery and diagnostic codes can be added here

            self.connection.commit()
            logging.info(f"Data committed to the database at {timestamp_str}.")

        except Exception as e:
            logging.error(f"Failed to insert data: {e}")
            self.connection.rollback()
        finally:
            self.cursor.close()
            self.connection.close()
            logging.info("Database connection closed.")

    def _insert_fuel_level(self, timestamp_id: int, fuel_level: Any) -> None:
        if fuel_level is not None:
            try:
                self.cursor.execute("""
                    INSERT INTO Fuel_level (User_Id, fuel, timestamp_id)
                    VALUES (%s, %s, %s);
                """, (self.userid, fuel_level, timestamp_id))
            except psycopg2.DatabaseError as e:
                logging.error(f"Failed to insert fuel level data: {e}")

    def _insert_fuel_cons(self, timestamp_id: int, consumption: Any) -> None:
        if consumption is not None:
            try:
                self.cursor.execute("""
                    INSERT INTO Fuel_cons (User_Id, consumption, timestamp_id)
                    VALUES (%s, %s, %s);
                """, (self.userid, consumption, timestamp_id))
            except psycopg2.DatabaseError as e:
                logging.error(f"Failed to insert fuel consumption data: {e}")

    def _insert_mass_air_flow(self, timestamp_id: int, air_flow: Any) -> None:
        if air_flow is not None:
            try:
                self.cursor.execute("""
                    INSERT INTO Mass_air_flow (User_Id, air_flow, timestamp_id)
                    VALUES (%s, %s, %s);
                """, (self.userid, air_flow, timestamp_id))
            except psycopg2.DatabaseError as e:
                logging.error(f"Failed to insert mass air flow data: {e}")

    def _insert_oxygen(self, timestamp_id: int, oxygen_level: Any) -> None:
        if oxygen_level is not None:
            try:
                self.cursor.execute("""
                    INSERT INTO Oxygen (User_Id, oxygen_level, timestamp_id)
                    VALUES (%s, %s, %s);
                """, (self.userid, oxygen_level, timestamp_id))
            except psycopg2.DatabaseError as e:
                logging.error(f"Failed to insert oxygen data: {e}")

    def _insert_speed(self, timestamp_id: int, speed: Any) -> None:
        if speed is not None:
            try:
                self.cursor.execute("""
                    INSERT INTO Speed_kph (User_Id, speed, timestamp_id)
                    VALUES (%s, %s, %s);
                """, (self.userid, speed, timestamp_id))
            except psycopg2.DatabaseError as e:
                logging.error(f"Failed to insert speed data: {e}")

    def _insert_throttle(self, timestamp_id: int, position: Any) -> None:
        if position is not None:
            try:
                self.cursor.execute("""
                    INSERT INTO Throttle (User_Id, position, timestamp_id)
                    VALUES (%s, %s, %s);
                """, (self.userid, position, timestamp_id))
            except psycopg2.DatabaseError as e:
                logging.error(f"Failed to insert throttle data: {e}")

    def _insert_coolant(self, timestamp_id: int, temp: Any) -> None:
        if temp is not None:
            try:
                self.cursor.execute("""
                    INSERT INTO Coolant (User_Id, temp, timestamp_id)
                    VALUES (%s, %s, %s);
                """, (self.userid, temp, timestamp_id))
            except psycopg2.DatabaseError as e:
                logging.error(f"Failed to insert coolant data: {e}")

    def _insert_intake_manifold(self, timestamp_id: int, level: Any) -> None:
        if level is not None:
            try:
                self.cursor.execute("""
                    INSERT INTO Intake_manifold (User_Id, level, timestamp_id)
                    VALUES (%s, %s, %s);
                """, (self.userid, level, timestamp_id))
            except psycopg2.DatabaseError as e:
                logging.error(f"Failed to insert intake manifold data: {e}")

    def _insert_rpm(self, timestamp_id: int, amount: Any) -> None:
        if amount is not None:
            try:
                self.cursor.execute("""
                    INSERT INTO RPM (User_Id, amount, timestamp_id)
                    VALUES (%s, %s, %s);
                """, (self.userid, amount, timestamp_id))
            except psycopg2.DatabaseError as e:
                logging.error(f"Failed to insert RPM data: {e}")
