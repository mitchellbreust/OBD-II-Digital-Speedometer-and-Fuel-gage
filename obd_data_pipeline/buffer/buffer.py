
class Buffer:
    def __init__(self) -> None:
        # Initialize a dictionary with empty lists for each data type
        self.data = {
            'fuel_level': [],
            'fuel_cons': [],
            'rpm': [],
            'coolant': [],
            'battery': [],
            'intake_manifold': [],
            'mass_air_flow': [],
            'oxygen': [],
            'speed': [],
            'throttle': [],
            'diagnostic_codes': []
        }

    def update_buffer(self, data: dict) -> None:
        # Iterate over the data dictionary and append values to the corresponding lists
        for key, value in data.items():
            if key in self.data:
                self.data[key].append(value)
            else:
                print(f"Warning: {key} is not a recognized data type and will be ignored.")

    def get_latest_data(self) -> dict:
        latest_data = {}
        for key, values in self.data.items():
            if values:  # If there are values in the list
                latest_data[key] = values[-1]  # Get the most recent value
        return latest_data

        
    def get_minimum_values(self) -> dict:
        min_values = {}
        for key, values in self.data.items():
            if values and key != 'diagnostic_codes':
                min_values[key] = min(values)
        return min_values

    def get_maximum_values(self) -> dict:
        max_values = {}
        for key, values in self.data.items():
            if values and key != 'diagnostic_codes':
                max_values[key] = max(values)
        return max_values

    def give_average_of_data(self) -> dict:
        # Calculate and return the average of each numeric data type
        averages = {}
        for key, values in self.data.items():
            if isinstance(values, list) and values and key != 'diagnostic_codes':
                if isinstance(values[0], (int, float)):  # Ensure the list contains numeric values
                    averages[key] = sum(values) / len(values)
        return averages

    def get_diagnostic_codes(self) -> list:
        return self.data['diagnostic_codes']

    def clear_buffer(self) -> None:
        # Clear all the lists in the data dictionary
        for key in self.data:
            self.data[key].clear()