import obd
from typing import Optional

def get_coolant_temp(connection: obd.OBD) -> Optional[float]:
    if not connection.supports(obd.commands.COOLANT_TEMP):
        print("Coolant Temperature command not supported by this vehicle.")
        return None
    
    response = connection.query(obd.commands.COOLANT_TEMP)
    
    if response.is_null():
        print("Failed to retrieve Coolant Temperature data.")
        return None
    
    coolant_temp_value = response.value.to("degC").magnitude  # Convert to degrees Celsius
    return coolant_temp_value
