import obd
from typing import Optional

def get_oxygen_sensor(connection: obd.OBD) -> Optional[float]:
    if not connection.supports(obd.commands.O2_B1S1):
        print("Oxygen Sensor (Bank 1, Sensor 1) command not supported by this vehicle.")
        return None
    
    response = connection.query(obd.commands.O2_B1S1)
    
    if response.is_null():
        print("Failed to retrieve Oxygen Sensor data.")
        return None
    
    oxygen_value = response.value.magnitude  # Typically in volts
    return oxygen_value
