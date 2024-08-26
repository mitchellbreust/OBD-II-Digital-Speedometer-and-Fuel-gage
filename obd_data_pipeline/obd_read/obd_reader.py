import obd
import sys
import logging
from typing import Optional, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ObdReader:
    def __init__(self, connection: obd.OBD) -> None:
        if not isinstance(connection, obd.OBD):
            raise TypeError("Connection must be an instance of obd.OBD.")
        
        self.connection = connection
        
        if not self.connection.is_connected():
            logging.error("OBD connection is not active.")
            raise ConnectionError("OBD connection is not active.")

    def query_obd(self, command: obd.commands.OBDCommand) -> Optional[obd.OBDResponse]:
        try:
            if not self.connection.supports(command):
                logging.warning(f"{command.name} command not supported by this vehicle.")
                return None
            
            response = self.connection.query(command)
            
            if response.is_null():
                logging.warning(f"Failed to retrieve data for {command.name}.")
                return None
            
            return response
        
        except Exception as e:
            logging.error(f"Error querying {command.name}: {e}")
            return None

    def get_battery_voltage(self) -> Optional[float]:
        response = self.query_obd(obd.commands.ELM_VOLTAGE)
        return response.value.magnitude if response else None

    def get_coolant_temp(self) -> Optional[float]:
        response = self.query_obd(obd.commands.COOLANT_TEMP)
        return response.value.to("degC").magnitude if response else None

    def get_diagnostic_codes(self) -> Optional[List[str]]:
        response = self.query_obd(obd.commands.GET_DTC)
        
        if response:
            dtc_list = response.value
            formatted_dtc_list = [f"{dtc[0]}: {dtc[1]}" for dtc in dtc_list]
            if not formatted_dtc_list:
                logging.info("No diagnostic trouble codes found.")
                return None
            return formatted_dtc_list
        return None

    def get_fuel_cons(self) -> Optional[float]:
        try:
            speed_response = self.query_obd(obd.commands.SPEED)
            maf_response = self.query_obd(obd.commands.MAF)

            if speed_response and maf_response:
                speed_kmh = speed_response.value.to("km/h").magnitude
                maf_magnitude = maf_response.value.magnitude

                air_fuel_ratio = 14.7
                fuel_cons_g_per_s = maf_magnitude / air_fuel_ratio
                fuel_cons_g_per_100km = (fuel_cons_g_per_s * 3600 * 100) / speed_kmh
                fuel_cons_l_per_100km = fuel_cons_g_per_100km / 735.5

                return fuel_cons_l_per_100km
            else:
                logging.warning("Failed to retrieve speed or MAF data.")
        except Exception as e:
            logging.error(f"Failed to calculate fuel consumption: {e}")
        return None

    def get_fuel_level(self) -> Optional[float]:
        response = self.query_obd(obd.commands.FUEL_LEVEL)
        return response.value.magnitude if response else None

    def get_intake_manifold_pressure(self) -> Optional[float]:
        response = self.query_obd(obd.commands.INTAKE_PRESSURE)
        return response.value.to("kPa").magnitude if response else None

    def get_maf(self) -> Optional[float]:
        response = self.query_obd(obd.commands.MAF)
        return response.value.to("g/s").magnitude if response else None

    def get_oxygen_sensor(self) -> Optional[float]:
        response = self.query_obd(obd.commands.O2_B1S1)
        return response.value.magnitude if response else None

    def get_rpm(self) -> Optional[float]:
        response = self.query_obd(obd.commands.RPM)
        return response.value.magnitude if response else None

    def get_speed(self) -> Optional[float]:
        response = self.query_obd(obd.commands.SPEED)
        return response.value.to('kmh').magnitude if response else None

    def get_throttle_position(self) -> Optional[float]:
        response = self.query_obd(obd.commands.THROTTLE_POS)
        return response.value.magnitude if response else None
