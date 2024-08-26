import obd
from datetime import datetime, timedelta
import time
from buffer.buffer import Buffer
from obd_read.obd_reader import ObdReader  # Fixed class name capitalization
from data_writer.database_writer import DatabaseWriter  # Fixed class name capitalization
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        connection = obd.OBD()
        if not connection.is_connected():
            logging.error("Failed to connect to OBD-II adapter.")
            return

        reader = ObdReader(connection)
        buff = Buffer()
        writer = DatabaseWriter()

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

            # Filter out None values
            filtered_data = {k: v for k, v in data.items() if v is not None}
            buff.update_buffer(filtered_data)

            current_time = datetime.now()
            if current_time - before_time >= timedelta(minutes=1):
                averages = buff.give_average_of_data()
                diagnostic_codes = buff.get_diagnostic_codes()
                writer.insert_new_data(before_time, averages)

                before_time = current_time
                buff.clear_buffer()

            time.sleep(0.5)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            logging.info("OBD-II connection closed.")

if __name__ == "__main__":
    main()