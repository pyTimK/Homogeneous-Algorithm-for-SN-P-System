from typing import Iterable

class Constants(set[int]):
    def scale(self, x: int):
        return Constants({x * c for c in self})

    def translate(self, x: int):
        return Constants({c + x for c in self})

    def mod(self, x: int):
        return Constants({c % x for c in self})

    def union(self, *s: "Constants") -> "Constants":
        return Constants(super().union(*s))

    def intersection(self, *s: "Constants") -> "Constants":
        return Constants(super().intersection(*s))

    def __sub__(constants1, constants2: "Constants") -> "Constants":
        return Constants(constants1.difference(constants2))