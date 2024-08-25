import obd
from typing import List, Optional

def get_diagnostic_codes(connection: obd.OBD) -> Optional[List[str]]:
    """
    Retrieves a list of Diagnostic Trouble Codes (DTCs) from the vehicle's OBD-II system.
    
    Parameters:
    - connection (obd.OBD): An active connection to the OBD-II interface.
    
    Returns:
    - List[str]: A list of DTCs, or None if no codes are present or if an error occurs.
    """
    # Check if the DTC command is supported
    if not connection.supports(obd.commands.GET_DTC):
        print("DTC command not supported by this vehicle.")
        return None
    
    # Query the vehicle for stored DTCs
    response = connection.query(obd.commands.GET_DTC)
    
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