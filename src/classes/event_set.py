from .event import Event
from .period_constants_pair import PeriodConstantsPair

class EventSet(set[Event]):
    def __hash__(self):
        return hash(tuple(self))
    
    def __eq__(self, other):
        return set(self) == set(other)
    