from typing import Tuple
from src.classes.rule_transition_set import RuleTransitionSet
from src.helpers.my_math import MyMath
from .get_parameters import get_parameters
from .compatible import compatible

#! ALGORITHM 4
def match(R: RuleTransitionSet, R_prime: RuleTransitionSet) -> Tuple[int, int, int, int]:
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

                u1_prime, t1, u2_prime, t2 = get_parameters(s.scale(m1), s_prime.scale(m2))
                u1, t1, u2, t2 = u1_prime * m1, t1, u2_prime * m2, t2

                if t1 == -1 or t2 == -1:
                    continue

                else:
                    if compatible(R.scale(u1).translate(t1), R.scale(u2).translate(t2)):
                        return u1, t1, u2, t2
                    
                    else:
                        continue

    return 2, 0, 2, 1