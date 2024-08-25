import obd
import sys
from typing import Optional

class Obd_reader:
    def __init__(self, connection: obd.OBD) -> None:
        self.connection = connection

    def get_battery_voltage(self) -> Optional[float]:
        if not self.connection.supports(obd.commands.ELM_VOLTAGE):
            print("Battery Voltage command not supported by this vehicle.")
            return None
        
        response = self.connection.query(obd.commands.ELM_VOLTAGE)
        
        if response.is_null():
            print("Failed to retrieve Battery Voltage data.")
            return None
        
        voltage_value = response.value.magnitude  # Battery voltage in volts
        return voltage_value

    def get_coolant_temp(self) -> Optional[float]:
        if not self.connection.supports(obd.commands.COOLANT_TEMP):
            print("Coolant Temperature command not supported by this vehicle.")
            return None
        
        response = self.connection.query(obd.commands.COOLANT_TEMP)
        
        if response.is_null():
            print("Failed to retrieve Coolant Temperature data.")
            return None
        
        coolant_temp_value = response.value.to("degC").magnitude  # Convert to degrees Celsius
        return coolant_temp_value

    def get_diagnostic_codes(self) -> Optional[List[str]]:
        # Check if the DTC command is supported
        if not self.connection.supports(obd.commands.GET_DTC):
            print("DTC command not supported by this vehicle.")
            return None
        
        # Query the vehicle for stored DTCs
        response = self.connection.query(obd.commands.GET_DTC)
        
        # Check if the response is valid
        if response.is_null():
            print("Failed to retrieve diagnostic codes.")
            return None
        
        # Extract the DTCs from the response
        dtc_list = response.value  # This is a list of tuples, each containing the DTC code and its description
        
        # Format the DTCs into a list of strings for easier display
        formatted_dtc_list = [f"{dtc[0]}: {dtc[1]}" for dtc in dtc_list]
        
        if not formatted_dtc_list:
            print("No diagnostic trouble codes found.")
            return None
        
        return formatted_dtc_list

    def get_fuel_cons(self) -> Optional[float]:
        try:
            # Query the OBD-II system for speed and MAF data
            speed_response = self.connection.query(obd.commands.SPEED)
            maf_response = self.connection.query(obd.commands.MAF)

            if not speed_response.is_null() and not maf_response.is_null():
                speed_kmh = speed_response.value.to("km/h").magnitude
                maf_magnitude = maf_response.value.magnitude

                # Calculate fuel consumption
                air_fuel_ratio = 14.7
                fuel_cons_g_per_s = maf_magnitude / air_fuel_ratio

                # Calculate fuel consumption in grams per 100 km
                fuel_cons_g_per_100km = (fuel_cons_g_per_s * 3600 * 100) / speed_kmh
                # Convert grams to liters (density of gasoline ~735.5 g/L)
                fuel_cons_l_per_100km = fuel_cons_g_per_100km / 735.5

                return fuel_cons_l_per_100km
            else:
                print("Failed to retrieve speed or MAF data.", file=sys.stderr)
        except Exception as e:
            print(f"Failed to get fuel consumption data: {e}", file=sys.stderr)
        return None

    def get_fuel_level(self) -> Optional[float]:
        try:
            cmd = obd.commands.FUEL_LEVEL
            res = self.connection.query(cmd)
            if res.value:
                return res.value.magnitude  # The fuel level as a percentage
        except Exception as e:
            print(f"Failed to get fuel level: {e}", file=sys.stderr)
        return None

    def get_intake_manifold_pressure(self) -> Optional[float]:
        if not self.connection.supports(obd.commands.INTAKE_PRESSURE):
            print("Intake Manifold Pressure command not supported by this vehicle.")
            return None
        
        response = self.connection.query(obd.commands.INTAKE_PRESSURE)
        
        if response.is_null():
            print("Failed to retrieve Intake Manifold Pressure data.")
            return None
        
        pressure_value = response.value.to("kPa").magnitude  # Convert to kPa
        return pressure_value

    def get_maf(self) -> Optional[float]:
        if not self.connection.supports(obd.commands.MAF):
            print("MAF command not supported by this vehicle.")
            return None
        
        # Query the MAF sensor
        response = self.connection.query(obd.commands.MAF)
        
        # Check if the response is valid
        if response.is_null():
            print("Failed to retrieve MAF data.")
            return None
        
        # Extract the MAF value in grams per second
        maf_value = response.value.to("g/s").magnitude
        return maf_value

    def get_oxygen_sensor(self) -> Optional[float]:
        if not self.connection.supports(obd.commands.O2_B1S1):
            print("Oxygen Sensor (Bank 1, Sensor 1) command not supported by this vehicle.")
            return None
        
        response = self.connection.query(obd.commands.O2_B1S1)
        
        if response.is_null():
            print("Failed to retrieve Oxygen Sensor data.")
            return None
        
        oxygen_value = response.value.magnitude  # Typically in volts
        return oxygen_value

    def get_rpm(self) -> Optional[float]:
        if not self.connection.supports(obd.commands.RPM):
            print("RPM command not supported by this vehicle.")
            return None
        
        response = self.connection.query(obd.commands.RPM)
        
        if response.is_null():
            print("Failed to retrieve RPM data.")
            return None
        
        rpm_value = response.value.magnitude  # RPM is typically returned as a simple numeric value
        return rpm_value

    def get_speed(self) -> Optional[float]:
        try:
            cmd = obd.commands.SPEED
            res = self.connection.query(cmd)
            if res.value:
                return res.value.to('kmh').magnitude

        except Exception as e:
            print(f"Failed to get speed: {e}", file=sys.stdin)
        return None

    def get_throttle_position(self) -> Optional[float]:
        if not self.connection.supports(obd.commands.THROTTLE_POS):
            print("Throttle Position command not supported by this vehicle.")
            return None
        
        response = self.connection.query(obd.commands.THROTTLE_POS)
        
        if response.is_null():
            print("Failed to retrieve Throttle Position data.")
            return None
        
        throttle_value = response.value.magnitude  # Throttle position as a percentage
        return throttle_value








        