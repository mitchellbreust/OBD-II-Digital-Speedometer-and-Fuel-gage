import obd
from typing import Optional

def get_throttle_position(connection: obd.OBD) -> Optional[float]:
    if not connection.supports(obd.commands.THROTTLE_POS):
        print("Throttle Position command not supported by this vehicle.")
        return None
    
    response = connection.query(obd.commands.THROTTLE_POS)
    
    if response.is_null():
        print("Failed to retrieve Throttle Position data.")
        return None
    
    throttle_value = response.value.magnitude  # Throttle position as a percentage
    return throttle_value
