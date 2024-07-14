import obd
from unittest.mock import MagicMock

# Mock connection class
class MockOBD(obd.OBD):
    def __init__(self, supported_commands):
        self.supported_commands = supported_commands
        self.query_responses = {}

    def query(self, command):
        if command in self.query_responses:
            return self.query_responses[command]
        return None

    def set_query_response(self, command, response):
        self.query_responses[command] = response

# Import your functions from obd_reader.py
from obd_reader import (
    get_speed,
    get_fuel_level,
    get_fuel_cons_via_mass_air_flow,
    get_fuel_cons_via_fuel_trim,
    get_fuel_cons_via_engine_load,
    get_fuel_consumption,
    is_fuel_cons_supported
)

def run_tests():
    # Create a mock connection
    supported_commands = {obd.commands.SPEED, obd.commands.FUEL_LEVEL, obd.commands.MAF, obd.commands.SHORT_FUEL_TRIM_1, obd.commands.LONG_FUEL_TRIM_1, obd.commands.ENGINE_LOAD, obd.commands.RPM}
    mock_connection = MockOBD(supported_commands)

    # Define mock responses
    speed_response = MagicMock()
    speed_response.value = MagicMock()
    speed_response.value.to.return_value = MagicMock(magnitude=60.0)  # 60 km/h

    fuel_level_response = MagicMock()
    fuel_level_response.value = MagicMock(magnitude=50.0)  # 50%

    maf_response = MagicMock()
    maf_response.value = MagicMock(magnitude=5.0)  # 5 g/s

    short_trim_response = MagicMock()
    short_trim_response.value = MagicMock(magnitude=5.0)  # 5%

    long_trim_response = MagicMock()
    long_trim_response.value = MagicMock(magnitude=5.0)  # 5%

    engine_load_response = MagicMock()
    engine_load_response.value = MagicMock(magnitude=80.0)  # 80%

    rpm_response = MagicMock()
    rpm_response.value = MagicMock(magnitude=3000.0)  # 3000 RPM

    # Set mock responses
    mock_connection.set_query_response(obd.commands.SPEED, speed_response)
    mock_connection.set_query_response(obd.commands.FUEL_LEVEL, fuel_level_response)
    mock_connection.set_query_response(obd.commands.MAF, maf_response)
    mock_connection.set_query_response(obd.commands.SHORT_FUEL_TRIM_1, short_trim_response)
    mock_connection.set_query_response(obd.commands.LONG_FUEL_TRIM_1, long_trim_response)
    mock_connection.set_query_response(obd.commands.ENGINE_LOAD, engine_load_response)
    mock_connection.set_query_response(obd.commands.RPM, rpm_response)

    # Run tests
    speed = get_speed(mock_connection)
    print(f"Test get_speed: {speed} km/h")

    fuel_level = get_fuel_level(mock_connection)
    print(f"Test get_fuel_level: {fuel_level} %")

    fuel_cons_maf = get_fuel_cons_via_mass_air_flow(mock_connection, speed)
    print(f"Test get_fuel_cons_via_mass_air_flow: {fuel_cons_maf} L/100km")

    fuel_cons_trim = get_fuel_cons_via_fuel_trim(mock_connection, speed)
    print(f"Test get_fuel_cons_via_fuel_trim: {fuel_cons_trim} L/100km")

    fuel_cons_load = get_fuel_cons_via_engine_load(mock_connection, speed)
    print(f"Test get_fuel_cons_via_engine_load: {fuel_cons_load} L/100km")

    fuel_consumption = get_fuel_consumption(mock_connection, speed)
    print(f"Test get_fuel_consumption: {fuel_consumption} L/100km")

    fuel_cons_supported = is_fuel_cons_supported(mock_connection)
    print(f"Test is_fuel_cons_supported: {fuel_cons_supported}")

if __name__ == "__main__":
    run_tests()
