class Constants(set[int]):
    def scale(self, x: int):
        return Constants({x * c for c in self})

    def translate(self, x: int):
        return Constants({c + x for c in self})

    def mod(self, x: int):
        return Constants({c % x for c in self})