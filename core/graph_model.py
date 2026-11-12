import csv #untuk membaca csv
import math
from dataclasses import asdict, dataclass
from pathlib import Path
@dataclass(frozen=True)
class Node:
    node_id: str
    device_name: str
    area: str
    floor: str
    function: str
    x: float
    y: float

    def to_dict(self):
        return asdict(self)