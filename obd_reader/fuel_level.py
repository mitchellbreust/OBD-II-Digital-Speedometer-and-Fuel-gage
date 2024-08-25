import obd
import sys
from typing import Optional


def get_fuel_level(connection: obd.OBD) -> Optional[float]:
    try:
        cmd = obd.commands.FUEL_LEVEL
        res = connection.query(cmd)
        if res.value:
            return res.value.magnitude  # The fuel level as a percentage
    except Exception as e:
        print(f"Failed to get fuel level: {e}", file=sys.stderr)
    return None
