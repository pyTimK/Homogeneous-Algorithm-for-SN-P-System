
class ConstantExp(int):
    """Exponent of the constant of a regular expression"""

class StarExpSet(set[int]):
    """Set of exponents of all stars of a regular expression"""
    #! Dunder Methods
    def __hash__(self):
        return hash(tuple(self))
    
    def __eq__(self, other):
        return set(self) == set(other)


class PlusExpSet(set[int]):
    """Set of exponents of all plus of a regular expression"""
    #! Dunder Methods
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
        """
        translates the regular expression of a rule

        Complexity: `O(1)`
        """
        rule_re_new: RuleRE = RuleRE()  #! O(1)
        for constant, star_set, plus_set in self:  #! O(1)
            new_constant = constant + x   #! O(1)
            rule_re_new.add((new_constant, star_set, plus_set))  #! O(1)
        
        return rule_re_new
    
    def scale(self, x: int):
        """
        scales the regular expression of a rule

        Complexity: `O(1)`
        """
        rule_re_new: RuleRE = RuleRE({})  #! O(1)
        for constant, star_set, plus_set in self:  #! O(1)
            new_constant = constant * x  #! O(1)
            new_star_set = StarExpSet({star * x for star in star_set})  #! O(1)
            new_plus_set = PlusExpSet({plus * x for plus in plus_set})  #! O(1)
            rule_re_new.add((new_constant, new_star_set, new_plus_set))  #! O(1)
        
        return rule_re_new
    
    #! Dunder Methods
    def __hash__(self):
        return hash(tuple(self))
    
    def __eq__(self, other):
        return set(self) == set(other)


    
