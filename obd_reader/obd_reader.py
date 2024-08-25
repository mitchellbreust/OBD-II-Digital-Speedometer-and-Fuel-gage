import obd
import sys
import time
from typing import Optional

connection = obd.OBD()

def is_command_supported(connection: obd.OBD, command) -> bool:
    return command in connection.supported_commands

def main_loop():
    speed_is_supported = is_command_supported(connection, obd.commands.SPEED)
    fuel_level_supported = is_command_supported(connection, obd.commands.FUEL_LEVEL)
    fuel_cons_supported = is_fuel_cons_supported(connection)

    speed = 0
    fuel = 0.00
    fuel_con = 0.00
    while True:
        if speed_is_supported:
            speed = get_speed(connection)
            if speed is None:
                print("Failed to get speed. Retrying...")
                time.sleep(0.1)
                speed = get_speed(connection)

        if fuel_level_supported:
            fuel = get_fuel_level(connection)
            if fuel is None:
                print("Failed to get fuel level. Retrying...")
                time.sleep(0.1)
                fuel = get_fuel_level(connection)

        if fuel_cons_supported and speed is not None:
            fuel_con = get_fuel_consumption(connection, speed)
            if fuel_con is None:
                print("Failed to estimate fuel consumption.")
        
        # Print the fetched data
        print(f"Speed: {speed:.2f} km/h, Fuel Level: {fuel:.2f} %, Fuel Consumption: {fuel_con:.2f} L/100km")

        # Wait for a specified interval before querying the data again
        time.sleep(0.2)
