import obd
import sys
from typing import Optional

def get_maf(connection: obd.OBD) -> Optional[float]:
    if not connection.supports(obd.commands.MAF):
        print("MAF command not supported by this vehicle.")
        return None
    
    # Query the MAF sensor
    response = connection.query(obd.commands.MAF)
    
    # Check if the response is valid
    if response.is_null():
        print("Failed to retrieve MAF data.")
        return None
    
    # Extract the MAF value in grams per second
    maf_value = response.value.to("g/s").magnitude
    return maf_value