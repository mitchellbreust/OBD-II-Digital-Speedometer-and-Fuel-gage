from itertools import cycle

class FakeOBD:
    def __init__(self):
        self.supported_commands = {
            'ELM_VOLTAGE': True,
            'COOLANT_TEMP': True,
            'RPM': True,
            'SPEED': True,
            'MAF': True,
            'O2_B1S1': True,
            'THROTTLE_POS': True,
            'INTAKE_PRESSURE': True,
            'FUEL_LEVEL': True,
            'GET_DTC': True,
        }

        # Define cycling values for each command
        self.fake_responses = {
            'ELM_VOLTAGE': cycle([12.4, 12.5, 12.6, 12.7]),
            'COOLANT_TEMP': cycle([85.0, 88.0, 90.0, 92.0]),
            'RPM': cycle([1500, 2000, 2500, 3000]),
            'SPEED': cycle([60.0, 70.0, 80.0, 90.0]),
            'MAF': cycle([1.8, 2.0, 2.2, 2.4]),
            'O2_B1S1': cycle([0.7, 0.8, 0.9, 1.0]),
            'THROTTLE_POS': cycle([20.0, 25.0, 30.0, 35.0]),
            'INTAKE_PRESSURE': cycle([95.0, 100.0, 105.0, 110.0]),
            'FUEL_LEVEL': cycle([45.0, 50.0, 55.0, 60.0]),
            'GET_DTC': cycle([[], [('P0300', 'Random/Multiple Cylinder Misfire Detected')]]),
        }

    def is_connected(self):
        return True

    def close(self):
        return True

    def supports(self, command):
        command_name = command.name if hasattr(command, 'name') else str(command)
        return self.supported_commands.get(command_name, False)

    def query(self, command):
        # Adjust the FakeResponse class to properly mimic the real OBD response structure
        class FakeResponse:
            def __init__(self, value):
                self.value = value

            def is_null(self):
                return self.value is None

            @property
            def magnitude(self):
                if isinstance(self.value, (int, float)):
                    return self.value
                return None

            def to(self, unit):
                # For simplicity, assume no unit conversion is needed
                return self

        class FakeValue:
            def __init__(self, magnitude):
                self.magnitude = magnitude

            def to(self, unit):
                return self  # Assume no unit conversion needed for simplicity

        command_name = command.name if hasattr(command, 'name') else str(command)
        # Cycle through the values for each command and wrap them in FakeValue
        response_value = next(self.fake_responses.get(command_name))
        if isinstance(response_value, list):  # For DTC codes, directly return the list
            return FakeResponse(response_value)
        return FakeResponse(FakeValue(response_value))
