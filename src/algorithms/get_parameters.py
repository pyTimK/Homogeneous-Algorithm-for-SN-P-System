from typing import Tuple
from src.classes.period_constants_pair import PeriodConstantsPair
from src.classes.constants import Constants

#! ALGORITHM 3
def get_parameters(s: PeriodConstantsPair, s_prime: PeriodConstantsPair) -> Tuple[int, int, int, int]:
    l, q_bar, q_bar_prime = s.get_combine_params(s_prime)

    if len(q_bar) <= len(q_bar_prime):
        u1, t1, u2, t2 = -1, -1, 1, 0

        for u1_prime in range(1, l + 2):
            for t1_prime in range(0, l):

                q_double_bar_prime = Constants()
                for l_mult in range(0, (u1_prime - 1) * l + 1, l):
                    for q_bar_prime_item in q_bar_prime:
                        q_double_bar_prime.add(q_bar_prime_item + l_mult)
                
                if q_bar.scale(u1_prime).translate(t1_prime).mod(l).issubset(q_double_bar_prime):
                    u1, t1, u2, t2 = u1_prime, t1_prime, u2, t2
                    return u1, t1, u2, t2

    else:
        u1, t1, u2, t2 = 1, 0, -1, -1

        for u2_prime in range(1, l + 2):
            for t2_prime in range(0, l):

                q_double_bar = Constants()
                for l_mult in range(0, (u2_prime - 1) * l + 1, l):
                    for q_bar_item in q_bar:
                        q_double_bar.add(q_bar_item + l_mult)
                
                if q_bar_prime.scale(u2_prime).translate(t2_prime).mod(l).issubset(q_double_bar):
                    u1, t1, u2, t2 = u1, t1, u2_prime, t2_prime
                    return u1, t1, u2, t2

    return u1, t1, u2, t2