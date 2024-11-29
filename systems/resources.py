from dataclasses import dataclass
from typing import Tuple

@dataclass
class DataResources:
    name: str
    position: Tuple[int, int]

class Cole:

    def __init__(self, pos):
        name = "cole"
        position = pos

        self.data = DataResources(
            name=name,
            position=position
        )