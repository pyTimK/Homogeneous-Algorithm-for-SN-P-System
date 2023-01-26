from copy import deepcopy
from .beta import Beta

class Event:
    """
    Represents the application of a rule.

    It is in the form `(α,β)` where `α` is the number of spikes consumed (negative) or received (positive),
    while `β = a^p:d = (p, d)` (spiking action with delay)
    """
    def __init__(self, consume: int, release: int, delay: int) -> None:
        self.alpha = consume
        self.beta = Beta(release, delay)

    # def __init__(self, consume: int, beta: Beta) -> None:
    #     self.alpha = consume
    #     self.beta = beta
    
    def __str__(self) -> str:
        return f"({self.alpha}, {self.beta})"
        # return f"Period: {self.period}\tConstants: {self.constants}"

    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Event):
            return self.alpha == __o.alpha and self.beta == __o.beta
        
        return False
    
    def __hash__(self):
        return hash((self.alpha, self.beta))
    
    def scale(self, x: int):
        return Event(self.alpha * x, self.beta.release, self.beta.delay)
