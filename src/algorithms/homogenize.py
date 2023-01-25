from typing import Set, Tuple
from src.classes.my_math import MyMath
from src.classes.rule_transition import RuleTransition
from src.classes.period_constants_pair import PeriodConstantsPair
from src.classes.constants import Constants
import copy

def homogenize(rules_input: Set[RuleTransition]) -> Set[RuleTransition]:

    rules = copy.deepcopy(rules_input)
    if len(rules) == 0:
        raise ValueError("Not a single rule is given")
    
    if len(rules) == 1:
        return rules

    R = rules.pop()

    for R_prime in rules:
        u1, t1, u2, t2 = match(R, R_prime)



def match(R: Set[RuleTransition], R_prime: Set[RuleTransition]) -> Tuple[int, int, int, int]:
     for r in R:
        for r_prime in R_prime:

            s = r.state
            alpha = r.event.alpha
            beta = r.event.beta

            s_prime = r_prime.state
            alpha_prime = r_prime.event.alpha
            beta_prime = r_prime.event.beta

            if beta != beta_prime:
                continue

            else:
                l = MyMath.lcm(abs(alpha), abs(alpha_prime))
                m1 = l // abs(alpha)
                m2 = l // abs(alpha_prime)

                u1_prime, t1, u2_prime, t2 = get_parameters(s.multiply(m1), s_prime.multiply(m2))
                u1, t1, u2, t2 = u1_prime * m1, t1, u2_prime * m2, t2

                if t1 == -1 or t2 == -1:
                    continue

                else:
                    # P = partition_events_set()
                    pass



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


