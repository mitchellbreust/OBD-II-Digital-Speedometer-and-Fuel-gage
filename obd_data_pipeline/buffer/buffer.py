import logging
from typing import Dict, List, Any, Optional, Union

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Buffer:
    def __init__(self) -> None:
        # Initialize a dictionary with empty lists for each data type
        self.data: Dict[str, List[Any]] = {
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

    def get_all_data(self):
        return self.data

    def update_buffer(self, data: Dict[str, Any]) -> None:
        # Iterate over the data dictionary and append values to the corresponding lists
        for key, value in data.items():
            if key in self.data:
                if isinstance(value, (int, float, str)):
                    self.data[key].append(value)
                elif key == 'diagnostic_codes' and isinstance(value, list) and all(isinstance(i, str) for i in value):
                    for v in value:
                        if v not in self.data[key]:
                            self.data[key].append(v)
                else:
                    logging.warning(f"Invalid value type for {key}: {type(value)}. Expected int, float, str, or list of strings.")
            else:
                logging.warning(f"{key} is not a recognized data type and will be ignored.")

    def get_latest_data(self) -> Dict[str, Optional[Any]]:
        latest_data: Dict[str, Optional[Any]] = {}
        for key, values in self.data.items():
            if values:  # If there are values in the list
                latest_data[key] = values[-1]  # Get the most recent value
            else:
                logging.info(f"No data available for {key}.")
                latest_data[key] = None
        return latest_data

    def get_minimum_values(self) -> Dict[str, Optional[Union[float, int]]]:
        min_values: Dict[str, Optional[Union[float, int]]] = {}
        for key, values in self.data.items():
            if values and isinstance(values[0], (int, float)):
                min_values[key] = min(values)
            else:
                logging.info(f"No valid data for minimum calculation for {key}.")
                min_values[key] = None
        return min_values

    def get_maximum_values(self) -> Dict[str, Optional[Union[float, int]]]:
        max_values: Dict[str, Optional[Union[float, int]]] = {}
        for key, values in self.data.items():
            if values and isinstance(values[0], (int, float)):
                max_values[key] = max(values)
            else:
                logging.info(f"No valid data for maximum calculation for {key}.")
                max_values[key] = None
        return max_values

    def give_average_of_data(self) -> Dict[str, Optional[float]]:
        # Calculate and return the average of each numeric data type
        averages: Dict[str, Optional[float]] = {}
        for key, values in self.data.items():
            if values and isinstance(values[0], (int, float)):  # Ensure that the values list contains numeric data
                averages[key] = sum(values) / len(values)
            else:
                averages[key] = None
        return averages

    def get_diagnostic_codes(self) -> List[str]:
        if self.data['diagnostic_codes']:
            return self.data['diagnostic_codes']
        else:
            logging.info("No diagnostic codes available.")
            return None

    def clear_buffer(self) -> None:
        # Clear all the lists in the data dictionary
        for key in self.data:
            self.data[key].clear()
        logging.info("Buffer cleared.")
