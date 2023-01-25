from .period_constants_pair import PeriodConstantsPair
from .event import Event

class RuleTransition:
    """Representation of a transition rule in the form `(s,e)` where `s` is a state in period-constants pair `(p, Q)` and `e` is the event `(α,β)`"""

    def __init__(self, s: PeriodConstantsPair, e: Event) -> None:
        self.state = s
        self.event = e

    def __str__(self) -> str:
        return f"({self.state}, {self.event})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, RuleTransition):
            return self.state == __o.state and self.event == __o.event
        
        return False
    
    def __hash__(self):
        return hash((self.state, self.event))