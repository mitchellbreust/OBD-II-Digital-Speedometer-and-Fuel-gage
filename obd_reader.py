import obd
import sys
import time
from typing import Optional

connection = obd.OBD()

def is_command_supported(connection: obd.OBD, command) -> bool:
    return command in connection.supported_commands


def get_speed(connection: obd.OBD) -> Optional[float]:
    try:
        cmd = obd.commands.SPEED
        res = connection.query(cmd)
        if res.value:
            return res.value.to('kmh').magnitude

    except Exception as e:
        print(f"Failed to get speed: {e}", file=sys.stdin)
    return None

def get_fuel_level(connection: obd.OBD) -> Optional[float]:
    try:
        cmd = obd.commands.FUEL_LEVEL
        res = connection.query(cmd)
        if res.value:
            return res.value.magnitude  # The fuel level as a percentage
    except Exception as e:
        print(f"Failed to get fuel level: {e}", file=sys.stderr)
    return None

# Function to calculate fuel consumption in L/100km using MAF data
def get_fuel_cons_via_mass_air_flow(connection: obd.OBD, speed_kmh: float) -> Optional[float]:
    try:
        cmd = obd.commands.MAF
        res = connection.query(cmd)
        if res.value:
            maf = res.value.magnitude  # MAF in grams/second
            air_fuel_ratio = 14.7
            fuel_cons_g_per_s = maf / air_fuel_ratio
            
            # Calculate fuel consumption in grams per 100 km
            fuel_cons_g_per_100km = (fuel_cons_g_per_s * 3600 * 100) / speed_kmh
            # Convert grams to liters (density of gasoline ~735.5 g/L)
            fuel_cons_l_per_100km = fuel_cons_g_per_100km / 735.5
            
            return fuel_cons_l_per_100km
    except Exception as e:
        print(f"Failed to get MAF: {e}", file=sys.stderr)
    return None

# Function to calculate fuel consumption in L/100km using fuel trim data
def get_fuel_cons_via_fuel_trim(connection: obd.OBD, speed_kmh: float) -> Optional[float]:
    try:
        short_trim_cmd = obd.commands.SHORT_FUEL_TRIM_1
        long_trim_cmd = obd.commands.LONG_FUEL_TRIM_1
        load_cmd = obd.commands.ENGINE_LOAD
        rpm_cmd = obd.commands.RPM

        short_trim_res = connection.query(short_trim_cmd)
        long_trim_res = connection.query(long_trim_cmd)
        load_res = connection.query(load_cmd)
        rpm_res = connection.query(rpm_cmd)

        if short_trim_res.value and long_trim_res.value and load_res.value and rpm_res.value:
            short_trim = short_trim_res.value.magnitude
            long_trim = long_trim_res.value.magnitude
            engine_load = load_res.value.magnitude
            rpm = rpm_res.value.magnitude

            # Calculate air-fuel ratio adjustment
            air_fuel_ratio = 14.7 * (1 + (short_trim + long_trim) / 100)
            # Calculate fuel flow rate in grams per second
            fuel_flow_rate_g_per_s = (engine_load / 100) * rpm * 0.5 / air_fuel_ratio
            # Convert fuel flow rate to grams per hour
            fuel_flow_rate_g_per_h = fuel_flow_rate_g_per_s * 3600
            # Calculate fuel consumption per 100 km
            fuel_cons_g_per_100km = (fuel_flow_rate_g_per_h * 100) / speed_kmh
            # Convert grams to liters (density of gasoline ~735.5 g/L)
            fuel_cons_l_per_100km = fuel_cons_g_per_100km / 735.5

            return fuel_cons_l_per_100km
    except Exception as e:
        print(f"Failed to get fuel trim data: {e}", file=sys.stderr)
    return None

# Function to calculate fuel consumption in L/100km using engine load data
def get_fuel_cons_via_engine_load(connection: obd.OBD, speed_kmh: float) -> Optional[float]:
    try:
        load_cmd = obd.commands.ENGINE_LOAD
        rpm_cmd = obd.commands.RPM

        load_res = connection.query(load_cmd)
        rpm_res = connection.query(rpm_cmd)

        if load_res.value and rpm_res.value:
            engine_load = load_res.value.magnitude
            rpm = rpm_res.value.magnitude

            # Calculate fuel flow rate in grams per second
            air_fuel_ratio = 14.7
            fuel_flow_rate_g_per_s = (engine_load / 100) * rpm * 0.5 / air_fuel_ratio
            # Convert fuel flow rate to grams per hour
            fuel_flow_rate_g_per_h = fuel_flow_rate_g_per_s * 3600
            # Calculate fuel consumption per 100 km
            fuel_cons_g_per_100km = (fuel_flow_rate_g_per_h * 100) / speed_kmh
            # Convert grams to liters (density of gasoline ~735.5 g/L)
            fuel_cons_l_per_100km = fuel_cons_g_per_100km / 735.5

            return fuel_cons_l_per_100km
    except Exception as e:
        print(f"Failed to get engine load data: {e}", file=sys.stderr)
    return None

# Main function to determine the best method to estimate fuel consumption
def get_fuel_consumption(connection: obd.OBD, speed_kmh: float) -> Optional[float]:
    if is_command_supported(connection, obd.commands.MAF):
        fuel_cons = get_fuel_cons_via_mass_air_flow(connection, speed_kmh)
        if fuel_cons is not None:
            return fuel_cons
    
    if is_command_supported(connection, obd.commands.SHORT_FUEL_TRIM_1) and is_command_supported(connection, obd.commands.LONG_FUEL_TRIM_1):
        fuel_cons = get_fuel_cons_via_fuel_trim(connection, speed_kmh)
        if fuel_cons is not None:
            return fuel_cons
    
    if is_command_supported(connection, obd.commands.ENGINE_LOAD) and is_command_supported(connection, obd.commands.RPM):
        fuel_cons = get_fuel_cons_via_engine_load(connection, speed_kmh)
        if fuel_cons is not None:
            return fuel_cons
    
    print("Failed to estimate fuel consumption using available methods.", file=sys.stderr)
    return None

def is_fuel_cons_supported(connection: obd.OBD) -> bool:
    if is_command_supported(connection, obd.commands.SHORT_FUEL_TRIM_1) and is_command_supported(connection, obd.commands.LONG_FUEL_TRIM_1):
        return True
    if is_command_supported(connection, obd.commands.ENGINE_LOAD) and is_command_supported(connection, obd.commands.RPM):
        return True
    return is_command_supported(connection, obd.commands.MAF)

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
        time.sleep(0.3)
