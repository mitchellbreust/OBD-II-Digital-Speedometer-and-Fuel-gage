import obd
from typing import Optional

def get_rpm(connection: obd.OBD) -> Optional[float]:
    if not connection.supports(obd.commands.RPM):
        print("RPM command not supported by this vehicle.")
        return None
    
    response = connection.query(obd.commands.RPM)
    
    if response.is_null():
        print("Failed to retrieve RPM data.")
        return None
    
    rpm_value = response.value.magnitude  # RPM is typically returned as a simple numeric value
    return rpm_value
