from typing import Set, List, Tuple, Iterable
from functools import reduce
from src.helpers.my_math import MyMath
from .constants import Constants

class PeriodConstantsPair:
    def __init__(self, period: int, constants: Constants) -> None:
        self.period = period
        self.constants = constants

    @staticmethod
    def empty():
        return PeriodConstantsPair(0, Constants())

    @staticmethod
    def intersection(*period_constants_pairs: "PeriodConstantsPair"):
        if len(period_constants_pairs) == 0:
            return PeriodConstantsPair.empty()
        
        if len(period_constants_pairs) == 1:
            return period_constants_pairs[0]
        
        union = PeriodConstantsPair.union(*period_constants_pairs)

        pcp0 = period_constants_pairs[0]
        l, q_intersection, _ = pcp0.get_combine_params(union)

        for i in range(1, len(period_constants_pairs)):
            pcp = period_constants_pairs[i]
            _, q_pcp, _ = pcp.get_combine_params(union)
            q_intersection = q_intersection.intersection(q_pcp)
        
        return PeriodConstantsPair(l, q_intersection)
    
    def __sub__(pcp1, pcp2: "PeriodConstantsPair"):
        if pcp1.is_empty() or pcp2.is_empty():
            return pcp1

        l, q_pcp1, q_pcp2 = pcp1.get_combine_params(pcp2)

        return PeriodConstantsPair(l, q_pcp1 - q_pcp2)



    @staticmethod
    def union(*period_constants_pairs: "PeriodConstantsPair"):
        # print(f"union called: {period_constants_pairs}")
        if len(period_constants_pairs) == 0:
            return PeriodConstantsPair.empty()
        
        if len(period_constants_pairs) == 1:
            return period_constants_pairs[0]
        
        # print(f"union return: {reduce(PeriodConstantsPair.__union_two, period_constants_pairs)}")

        return reduce(PeriodConstantsPair.__union_two, period_constants_pairs)

    @staticmethod
    def __union_two(pcp1: "PeriodConstantsPair", pcp2: "PeriodConstantsPair"):
        l, q_bar, q_bar_prime = pcp1.get_combine_params(pcp2)
        
        return PeriodConstantsPair(l, q_bar.union(q_bar_prime))


    def get_combine_params(pcp1, pcp2: "PeriodConstantsPair") -> Tuple[int, Constants, Constants]:
        p, q, p_prime, q_prime = pcp1.period, pcp1.constants, pcp2.period, pcp2.constants
        l = MyMath.lcm(p, p_prime)
        q_bar= Constants()
        q_bar_prime= Constants()
        for p_mult in range(0, l - p + 1, p):
            for q_item in q:
                q_bar.add(q_item + p_mult)

        for p_prime_mult in range(0, l - p_prime + 1, p_prime):
            for q_prime_item in q_prime:
                q_bar_prime.add(q_prime_item + p_prime_mult)
        
        return l, q_bar, q_bar_prime
    

    def is_empty(self):
        return len(self.constants) == 0

    def scale(self, x: int):
        return PeriodConstantsPair(self.period * x, self.constants.scale(x))

    def translate(self, x: int):
        return PeriodConstantsPair(self.period, self.constants.translate(x))


    def __str__(self) -> str:
        return f"({self.period}, {self.constants})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, PeriodConstantsPair):
            return self.period == __o.period and self.constants == __o.constants
        
        return False
    
    def __hash__(self):
        return hash((self.period, frozenset(self.constants)))
    