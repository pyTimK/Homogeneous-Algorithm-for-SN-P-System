from collections import OrderedDict

class Position:
    """Contains the x and y coordinates of a neuron"""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def from_json(cls, position_json: OrderedDict[str, str]):
        return cls(float(position_json["x"]), float(position_json["y"]))

    def get_translate(self, dx: float, dy: float):
        return Position(self.x + dx, self.y + dy)

