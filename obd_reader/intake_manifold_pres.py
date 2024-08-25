import obd
from typing import Optional

def get_intake_manifold_pressure(connection: obd.OBD) -> Optional[float]:
    if not connection.supports(obd.commands.INTAKE_PRESSURE):
        print("Intake Manifold Pressure command not supported by this vehicle.")
        return None
    
    response = connection.query(obd.commands.INTAKE_PRESSURE)
    
    if response.is_null():
        print("Failed to retrieve Intake Manifold Pressure data.")
        return None
    
    pressure_value = response.value.to("kPa").magnitude  # Convert to kPa
    return pressure_value
