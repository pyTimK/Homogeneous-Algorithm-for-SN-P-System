from .parition_events import PartitionEvents
from .period_constants_pair import PeriodConstantsPair

class PartitionEventsSet(set[PartitionEvents]):

    def scope(self):
        return PeriodConstantsPair.union(*[pes.block for pes in self])
    