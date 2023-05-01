from .rule import Rule
from src.types.ruleset_str import RuleSetStr
from typing import Optional

class RuleSet(set[Rule]):
    """
    Represents a set of rules

    Note that there could be a maximum of `nk` rules a RuleSet can have
    """
    #! Operations
    def union(self, *rule_set_tuple: "RuleSet"):
        """
        combines two or more rule sets

        Complexity: `O(nk)`
        """
        return RuleSet(super().union(*rule_set_tuple))  #! O(nk)
    
    def translate(self, x: int):
        """
        translates each rule in the rule set

        Complexity: `O(k)`
        """
        return RuleSet({rt.translate(x) for rt in self})  #! O(k)
    
    def scale(self, x: int):
        """
        scale each rule in the rule set

        Complexity: `O(k)`
        """
        
        return RuleSet({rt.scale(x) for rt in self})  #! O(k)
    
    #! Parsing
    @staticmethod
    def from_str(rule_set_str: Optional[RuleSetStr]):
        """
        Converts the input rule set string to its equivalent RuleSet object

        Complexity: `O(k)`
        """
        if rule_set_str == None:  #! O(1)
            return RuleSet()  #! O(1)
        
        rule_str_list = rule_set_str.split(" ")  #! O(k)
        return RuleSet({Rule.from_dict(rule_str) for rule_str in rule_str_list})  #! O(k)


    def to_xmp(self):
        """
        Converts the Neuron object to its equivalent xmp string
        """
    
    #! Dunder Methods
    def __str__(self) -> str:
        return f"{set(self)}"

    def __repr__(self) -> str:
        return self.__str__()
    
    def __hash__(self):
        return hash(tuple(self))
    
    def __eq__(self, other):
        return set(self) == set(other)
    

