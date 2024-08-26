import obd
from datetime import datetime, timedelta
import time
from buffer.buffer import Buffer
from obd_read.obd_reader import Obd_reader
from data_writer.database_writer import Database_writer
from typing import Optional

def main():
    connection = obd.OBD()
    reader = Obd_reader(connection)
    buff = Buffer()
    writter = Database_writer()

    before_time = datetime.now()
    while True:
        data = {
            'fuel_level': reader.get_fuel_level(),
            'fuel_cons': reader.get_fuel_cons(),
            'rpm': reader.get_rpm(),
            'coolant': reader.get_coolant_temp(),
            'battery': reader.get_battery_voltage(),
            'intake_manifold': reader.get_intake_manifold_pressure(),
            'mass_air_flow': reader.get_maf(),
            'oxygen': reader.get_oxygen_sensor(),
            'speed': reader.get_speed(),
            'throttle': reader.get_throttle_position(),
            'diagnostic_codes': reader.get_diagnostic_codes()
        }
        buff.update_buffer(data)

        current_time = datetime.now()
        if current_time - before_time >= timedelta(minutes=1):
            averages = buff.give_average_of_data()
            diagnostic_codes = buff.get_diagnostic_codes()
            writter.insert_new_data(before_time, averages)

            before_time = current_time
            buff.clear_buffer()

        time.sleep(0.5)

        