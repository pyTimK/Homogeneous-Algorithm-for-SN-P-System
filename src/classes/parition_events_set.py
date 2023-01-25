from typing import Set
from .period_constants_pair import PeriodConstantsPair
from .event import Event

class PartitionEventsSet:
    def __init__(self, block: PeriodConstantsPair, events: Set[Event]) -> None:
        self.block =  block
        self.events = events

    def __str__(self) -> str:
        return f"({self.block}, {self.events})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, PartitionEventsSet):
            return self.block == __o.block and self.events == __o.events
        
        return False
    
    def __hash__(self):
        return hash((self.block, frozenset(self.events)))