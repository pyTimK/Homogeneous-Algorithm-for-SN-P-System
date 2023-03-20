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
    
    @staticmethod
    def union(*s: "Constants") -> "Constants":
        result = set()
        for constants in s:
            result |= constants
        return Constants(result)
    
    @staticmethod
    def intersection(*s: "Constants") -> "Constants":
        if len(s) == 0:
            return Constants(set())
        
        if len(s) == 1:
            return s[0]
        
        result = set(s[0])
        for constants in s[1:]:
            result &= constants
        return Constants(result)