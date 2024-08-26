import random

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

        # Define possible random values for each command
        self.fake_responses = {
            'ELM_VOLTAGE': [12.4, 12.5, 12.6, 12.7, 12.8, 12.9, 13.0, 13.1, 13.2, 13.3],
            'COOLANT_TEMP': [85.0, 88.0, 90.0, 92.0, 93.0, 95.0, 96.0, 98.0, 100.0],
            'RPM': [1500, 2000, 2500, 3000, 3200, 3400, 3600, 3800, 4000, 4200],
            'SPEED': [60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0],
            'MAF': [1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6],
            'O2_B1S1': [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5],
            'THROTTLE_POS': [20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0],
            'INTAKE_PRESSURE': [95.0, 100.0, 105.0, 110.0, 115.0, 120.0, 125.0, 130.0, 135.0],
            'FUEL_LEVEL': [45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0],
            'GET_DTC': [
                [],
                [('P0300', 'Random/Multiple Cylinder Misfire Detected')],
                [('P0130', 'O2 Sensor Circuit Malfunction')],
                [('P0171', 'System Too Lean')],
                [('P0420', 'Catalyst System Efficiency Below Threshold')],
                [('P0440', 'Evaporative Emission Control System Malfunction')]
            ],
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
        # Randomly select a value from the list of possible responses
        response_value = random.choice(self.fake_responses.get(command_name))
        if isinstance(response_value, list):  # For DTC codes, directly return the list
            return FakeResponse(response_value)
        return FakeResponse(FakeValue(response_value))
