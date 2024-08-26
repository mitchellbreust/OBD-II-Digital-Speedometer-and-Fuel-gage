import psycopg2


class Database_writer:
    def __init__(self, dbname, user, password, userid) -> None:
        self.connection = psycopg2.connect(dbname=dbname, user=user, password=password)
        self.cursor = self.connection.cursor()
        self.userid = userid

    def insert_new_data(self, timestamp, data):
        # Convert the timestamp to the format that matches the database
        timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')

        # Check if the timestamp row exists
        self.cursor.execute("""
            SELECT id FROM timestamps WHERE timestamp = %s;
        """, (timestamp_str,))
        result = self.cursor.fetchone()

        if result:
            # Timestamp exists, get the id
            timestamp_id = result[0]
        else:
            # Timestamp does not exist, insert a new row and get the id
            self.cursor.execute("""
                INSERT INTO timestamps (timestamp) VALUES (%s) RETURNING id;
            """, (timestamp_str,))
            timestamp_id = self.cursor.fetchone()[0]

        insert_fuel_level(self.cursor, self.userid, timestamp_id, data['fuel_level'])
        insert_fuel_cons(self.cursor, self.userid, timestamp_id, data[ 'fuel_cons'])
        insert_rpm(self.cursor, self.userid, timestamp_id, data['rpm'])
        insert_coolant(self.cursor, self.userid, timestamp_id, data['coolant'])
        # need battery, do later
        insert_intake_manifold(self.cursor, self.userid, timestamp_id, data['intake_manifold'])
        insert_mass_air_flow(self.cursor, self.userid, timestamp_id, data['mass_air_flow'])
        insert_oxygen(self.cursor, self.userid, timestamp_id, data['oxygen'])
        insert_speed_kph(self.cursor, self.userid, timestamp_id, data['speed'])
        insert_throttle(self.cursor, self.userid, timestamp_id, data['throttle'])
        # need diagnostic codes, do later

        self.connection.commit()


def insert_fuel_level(cursor, userid, timestamp_id, fuel_level):
    if not fuel_level:
        return
    cursor.execute("""
        INSERT INTO Fuel_level (User_Id, fuel, timestamp_id)
        VALUES (%s, %s, %s);
    """, (userid, fuel_level, timestamp_id))

def insert_fuel_cons(cursor, userid, timestamp_id, consumption):
    if not consumption:
        return
    cursor.execute("""
        INSERT INTO Fuel_cons (User_Id, consumption, timestamp_id)
        VALUES (%s, %s, %s);
    """, (userid, consumption, timestamp_id))


def insert_mass_air_flow(cursor, userid, timestamp_id, air_flow):
    if not air_flow:
        return
    cursor.execute("""
        INSERT INTO Mass_air_flow (User_Id, air_flow, timestamp_id)
        VALUES (%s, %s, %s);
    """, (userid, air_flow, timestamp_id))

def insert_oxygen(cursor, userid, timestamp_id, oxygen_level):
    if not oxygen_level:
        return
    cursor.execute("""
        INSERT INTO Oxygen (User_Id, oxygen_level, timestamp_id)
        VALUES (%s, %s, %s);
    """, (userid, oxygen_level, timestamp_id))

def insert_speed_kph(cursor, userid, timestamp_id, speed):
    if not speed:
        return
    cursor.execute("""
        INSERT INTO Speed_kph (User_Id, speed, timestamp_id)
        VALUES (%s, %s, %s);
    """, (userid, speed, timestamp_id))

def insert_throttle(cursor, userid, timestamp_id, position):
    if not position:
        return
    cursor.execute("""
        INSERT INTO Throttle (User_Id, position, timestamp_id)
        VALUES (%s, %s, %s);
    """, (userid, position, timestamp_id))

def insert_coolant(cursor, userid, timestamp_id, temp):
    if not temp:
        return
    cursor.execute("""
        INSERT INTO Coolant (User_Id, temp, timestamp_id)
        VALUES (%s, %s, %s);
    """, (userid, temp, timestamp_id))

def insert_intake_manifold(cursor, userid, timestamp_id, level):
    if not level:
        return
    cursor.execute("""
        INSERT INTO Intake_manifold (User_Id, level, timestamp_id)
        VALUES (%s, %s, %s);
    """, (userid, level, timestamp_id))

def insert_rpm(cursor, userid, timestamp_id, amount):
    if not amount:
        return
    cursor.execute("""
        INSERT INTO RPM (User_Id, amount, timestamp_id)
        VALUES (%s, %s, %s);
    """, (userid, amount, timestamp_id))
