import obd
import sys
from typing import Optional

connection = obd.OBD()

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

            air_fuel_ratio = 14.7 * (1 + (short_trim + long_trim) / 100)
            fuel_consumption_per_s = (engine_load * rpm * 0.5) / air_fuel_ratio  # Estimated grams per second
            fuel_consumption_per_100km = (fuel_consumption_per_s * 3600 * 100) / speed_kmh
            fuel_consumption_per_100km_l = fuel_consumption_per_100km / 735.5  # Convert to liters

            return fuel_consumption_per_100km_l
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
            engine_load = load_res.value.magnitude / 100  # Engine load as a fraction
            rpm = rpm_res.value.magnitude

            # Estimate fuel consumption based on engine load and RPM
            air_fuel_ratio = 14.7
            fuel_cons_g_per_s = (engine_load * rpm * 0.5) / air_fuel_ratio  # grams per second
            fuel_cons_g_per_100km = (fuel_cons_g_per_s * 3600 * 100) / speed_kmh
            fuel_cons_l_per_100km = fuel_cons_g_per_100km / 735.5  # Convert to liters

            return fuel_cons_l_per_100km
    except Exception as e:
        print(f"Failed to get engine load data: {e}", file=sys.stderr)
    return None

# Main function to determine the best method to estimate fuel consumption
def get_fuel_consumption(connection: obd.OBD, speed_kmh: float) -> Optional[float]:
    fuel_cons = get_fuel_cons_via_mass_air_flow(connection, speed_kmh)
    if fuel_cons is not None:
        return fuel_cons
    
    fuel_cons = get_fuel_cons_via_fuel_trim(connection, speed_kmh)
    if fuel_cons is not None:
        return fuel_cons
    
    fuel_cons = get_fuel_cons_via_engine_load(connection, speed_kmh)
    if fuel_cons is not None:
        return fuel_cons
    
    print("Failed to estimate fuel consumption using available methods.", file=sys.stderr)
    return None