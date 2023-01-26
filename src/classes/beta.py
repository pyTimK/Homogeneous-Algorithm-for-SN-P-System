
class Beta:
    """
    Part of an event that represents the spiking action with delay `β = a^p:d = (p, d)`
    """
    def __init__(self, release: int, delay: int) -> None:
        self.release = release
        self.delay = delay
    
    def __str__(self) -> str:
        return f"({self.release}, {self.delay})"
        # return f"Period: {self.period}\tConstants: {self.constants}"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Beta):
            return self.release == __o.release and self.delay == __o.delay
        
        return False

    def __hash__(self):
        return hash((self.release, self.delay))