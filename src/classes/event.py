from copy import deepcopy

class Event:
    """
    Represents the application of a rule.

    It is in the form `(α,β)` where `α` is the number of spikes consumed (negative) or received (positive),
    while `β = a^p:d = (p, d)` (spiking action with delay)
    """
    def __init__(self, consume: int, release: int, delay: int) -> None:
        self.alpha = consume
        self.beta = Beta(release, delay)
    
    def __str__(self) -> str:
        return f"({self.alpha}, {self.beta})"
        # return f"Period: {self.period}\tConstants: {self.constants}"

    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Event):
            return self.consume == __o.consume and self.beta == __o.beta
        
        return False
    
    def __hash__(self):
        return hash((self.consume, self.beta))
    
    def scale(self, x: int):
        return Event(self.alpha * x, deepcopy(self.beta))

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