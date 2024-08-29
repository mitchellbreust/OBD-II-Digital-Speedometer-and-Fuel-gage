import obd
import logging
from datetime import datetime, timedelta
import time
from buffer.buffer import Buffer
from obd_read.obd_reader import ObdReader
from data_writer.database_writer import DatabaseWriter
from test.fake_obd import FakeOBD

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(connection=None):
    try:
        # Use the provided connection or default to a real OBD connection
        connection = connection or obd.OBD()
        if connection.is_connected():
            print("Connected to OBD-II adapter")
        else:
            connection = obd.OBD("/dev/ttyACM0")
        if not connection.is_connected():
            logging.error("Failed to connect to OBD-II adapter.")
            return
        
        reader = ObdReader(connection)
        buff = Buffer()
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

            filtered_data = {k: v for k, v in data.items() if v is not None}
            buff.update_buffer(filtered_data)

            current_time = datetime.now()
            if current_time - before_time >= timedelta(seconds=5):  # Changed from minutes=1 to seconds=10:
                averages = buff.give_average_of_data()
                diagnostics = buff.get_diagnostic_codes()
                if diagnostics:
                    averages['diagnostic_codes'] = diagnostics

                writer = DatabaseWriter(dbname="car_data", user="mitchellbreust", userid=1)
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
    if input(str("Test? ")).lower() == "yes":
        fake_connection = FakeOBD()
        main(connection=fake_connection)
    else:
        main()
