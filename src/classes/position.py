from src.types.position_dict import PositionDict

class Position():
    """Contains the x and y coordinates of a neuron"""
    
    def __init__(self, x: float, y: float) -> None:
        """
        Initializes a position

        Complexity: `O(1)`
        """
        self.x = x  #! O(1)
        self.y = y  #! O(1)

    #! Dunder Methods
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return self.__str__()

    #! Parsing
    @staticmethod
    def from_dict(position_dict: PositionDict):
        """
        Converts the input position dictionary to its equivalent Position object

        Complexity: `O(1)`
        """
        return Position(float(position_dict.get("x")), float(position_dict.get("y")))  #! O(1)

    def get_translate(self, dx: float, dy: float):
        """
        Translates a position by dx horizontally and dy vertically

        Complexity: `O(1)`
        """
        return Position(self.x + dx, self.y + dy)  #! O(1)

