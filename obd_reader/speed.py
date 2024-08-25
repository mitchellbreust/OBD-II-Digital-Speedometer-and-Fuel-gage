import obd
import sys
from typing import Optional

def get_speed(connection: obd.OBD) -> Optional[float]:
    try:
        cmd = obd.commands.SPEED
        res = connection.query(cmd)
        if res.value:
            return res.value.to('kmh').magnitude

    except Exception as e:
        print(f"Failed to get speed: {e}", file=sys.stdin)
    return None
