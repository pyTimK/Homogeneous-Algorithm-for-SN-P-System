
class ConstantExp(int):
    """Exponent of the constant of a regular expression"""

class StarExpSet(set[int]):
    """Set of exponents of all stars of a regular expression"""
    def __hash__(self):
        return hash(tuple(self))
    
    def __eq__(self, other):
        return set(self) == set(other)


class PlusExpSet(set[int]):
    """Set of exponents of all plus of a regular expression"""
    def __hash__(self):
        return hash(tuple(self))
    
    def __eq__(self, other):
        return set(self) == set(other)




class RuleRE(set[tuple[ConstantExp, StarExpSet, PlusExpSet]]):
    """Regular expression of a rule \n
    ex: \n
    3a -> {(3,{},{})} \\
    2a(3a)*(4a)*(5a)+ -> {(2,{3,4},{5})} \\
    4a3a(3a)* U (2a)*(5a)+ -> {(7,{3},{}),(0,{2},{5})}
    """

    def translate(self, x: int):
        rule_re_new: RuleRE = RuleRE()
        for constant, star_set, plus_set in self:
            new_constant = constant + x 
            rule_re_new.add((new_constant, star_set, plus_set))
        
        return rule_re_new
    
    def scale(self, x: int):
        rule_re_new: RuleRE = RuleRE({})
        for constant, star_set, plus_set in self:
            new_constant = constant * x
            new_star_set = StarExpSet({star * x for star in star_set})
            new_plus_set = PlusExpSet({plus * x for plus in plus_set})
            rule_re_new.add((new_constant, new_star_set, new_plus_set))
        
        return rule_re_new
    
    def __hash__(self):
        return hash(tuple(self))
    
    def __eq__(self, other):
        return set(self) == set(other)


    
