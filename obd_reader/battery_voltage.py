def get_battery_voltage(connection: obd.OBD) -> Optional[float]:
    if not connection.supports(obd.commands.ELM_VOLTAGE):
        print("Battery Voltage command not supported by this vehicle.")
        return None
    
    response = connection.query(obd.commands.ELM_VOLTAGE)
    
    if response.is_null():
        print("Failed to retrieve Battery Voltage data.")
        return None
    
    voltage_value = response.value.magnitude  # Battery voltage in volts
    return voltage_value
