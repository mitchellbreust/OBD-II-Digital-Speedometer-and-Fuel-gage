import sys
from typing import Optional
# Function to calculate fuel consumption in L/100km using MAF data
def get_fuel_cons(speed_kmh: float, maf_magnitude) -> Optional[float]:
    try:
            air_fuel_ratio = 14.7
            fuel_cons_g_per_s = maf_magnitude / air_fuel_ratio
            
            # Calculate fuel consumption in grams per 100 km
            fuel_cons_g_per_100km = (fuel_cons_g_per_s * 3600 * 100) / speed_kmh
            # Convert grams to liters (density of gasoline ~735.5 g/L)
            fuel_cons_l_per_100km = fuel_cons_g_per_100km / 735.5
            
            return fuel_cons_l_per_100km
    except Exception as e:
        print(f"Failed to get MAF: {e}", file=sys.stderr)
    return None

