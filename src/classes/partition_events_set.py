from .partition_events import PartitionEvents
from .period_constants_pair import PeriodConstantsPair

class PartitionEventsSet(set[PartitionEvents]):

    def scope(self):
        return PeriodConstantsPair.union_unbounded(*[pes.block for pes in self])
    