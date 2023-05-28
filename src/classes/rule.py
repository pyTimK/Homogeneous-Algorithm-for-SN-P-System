
import re
from .rule_re import RuleRE, ConstantExp, PlusExpSet, StarExpSet
from typing import List, Set

class Rule:
    """
    Represents a rule in a neuron of an SN P system
    """

    __symbol = "a"
    __re_delimeter = "U"

    def __init__(self, rule_re: RuleRE, consume: int, release: int, delay: int) -> None:
        """
        Initializes a rule

        Complexity: `O(1)`
        """
        self. rule_re = rule_re  #! O(1)
        self.consume = consume  #! O(1)
        self.release = release  #! O(1)
        self.delay = delay  #! O(1)


    #! Parsing
    @staticmethod
    def from_dict(rule_str: str):
        """
        Converts the input rule dictionary to its equivalent Rule object

        Complexity: `O(1)`
        """

        match = re.match(fr"(.*)/(\w+)->(\w*);(\w*)", rule_str)
        rule_re_str, consume_str, release_str, delay_str = match.groups()

        rule_re = Rule.__get_rule_re(rule_re_str)
        consume = Rule.__get_consume(consume_str)
        release = Rule.__get_release(release_str)
        delay = Rule.__get_delay(delay_str)

        return Rule(rule_re, consume, release, delay)

    
    @staticmethod
    def __get_rule_re(re_str: str) -> RuleRE:
        re_list: List[str] = re_str.split(Rule.__re_delimeter)

        rule_re: RuleRE = RuleRE({})

        for reg_exp in re_list:
            #? Star Set
            # print(reg_exp)
            star_pattern = r"\(([^()]+)\)\*"
            stars_str: List[str] = re.findall(star_pattern, reg_exp)
            reg_exp = re.sub(star_pattern, "", reg_exp)
            star_set: StarExpSet = StarExpSet({1 if x == "a" else int(x.replace("a", "")) for x in stars_str})
            # print(reg_exp)
            #? Plus Set
            plus_pattern = r"\(([^()]+)\)\+"
            pluses_str: List[str] = re.findall(plus_pattern, reg_exp)
            # print(pluses_str)
            reg_exp = re.sub(plus_pattern, "", reg_exp)
            plus_set: PlusExpSet = PlusExpSet({1 if x == "a" else int(x.replace("a", "")) for x in pluses_str})

            #? Bounded List
            # print(unb_reg_exp)
            reg_exp = reg_exp.replace('(', '')
            reg_exp = reg_exp.replace(')', '')
            # print(unb_reg_exp)
            constant_str = reg_exp.split(Rule.__symbol)[:-1]
            constant_list: List[int] = [1 if x == "" else int(x) for x in constant_str]
            constant = sum(constant_list)

            rule_re.add((constant, star_set, plus_set))

        return rule_re
    
    @staticmethod
    def __get_constant_str(exponent: int):
        if exponent == 0:
            return ""
        
        if exponent == 1:
            return Rule.__symbol
        
        return f"{exponent}{Rule.__symbol}"

    @staticmethod
    def __get_star_str(exponent: int):
        if exponent == 0:
            return ""
        
        if exponent == 1:
            return f"({Rule.__symbol})*"
        
        return f"({exponent}{Rule.__symbol})*"
    
    @staticmethod
    def __get_plus_str(exponent: int):
        if exponent == 0:
            return ""
        
        if exponent == 1:
            return f"({Rule.__symbol})+"
        
        return f"({exponent}{Rule.__symbol})+"

    @staticmethod
    def __get_re_str(rule_re: RuleRE):
        re_union_list: List[str] = []

        for rule_re_tuple in rule_re:
            constant, star_set, plus_set = rule_re_tuple

            re_str = ""

            constant_str = Rule.__get_constant_str(constant)
            re_str += constant_str

            for star in star_set:
                star_str = Rule.__get_star_str(star)
                re_str += star_str
            
            for plus in plus_set:
                plus_str = Rule.__get_plus_str(plus)
                re_str += plus_str
            
            re_union_list.append(re_str)

        re_union_str = Rule.__re_delimeter.join(re_union_list)
        
        return re_union_str

    @staticmethod
    def __get_consume(consume_str: str):
        if consume_str == Rule.__symbol:
            return 1

        return int(consume_str.replace(Rule.__symbol, ""))
    
    @staticmethod
    def __get_consume_str(consume: int) -> str:
        if consume == 1:
            return Rule.__symbol
        
        return f"{consume}{Rule.__symbol}"
    
    @staticmethod
    def __get_release(release_str: str):
        if release_str == "0":
            return 0

        if release_str == Rule.__symbol:
            return 1
        
        return int(release_str.replace(Rule.__symbol, ""))


    @staticmethod
    def __get_release_str(release: int) -> str:
        if release == 0:
            return "0"

        if release == 1:
            return Rule.__symbol
        
        return f"{release}{Rule.__symbol}"

    
    @staticmethod
    def __get_delay(delay_str: str):
        return int(delay_str)
    
    @staticmethod
    def __get_delay_str(delay: int) -> str:
        return str(delay)

    def to_xmp_str(self):
        re_str = Rule.__get_re_str(self.rule_re)
        consume_str = Rule.__get_consume_str(self.consume)
        release_str = Rule.__get_release_str(self.release)
        delay_str = Rule.__get_delay_str(self.delay)

        rule_str = f"{re_str}/{consume_str}->{release_str};{delay_str}"
        return rule_str
    


    #! Operations
    def translate(self, x: int):
        """
        translates a rule

        Complexity: `O(1)`
        """
        return Rule(self.rule_re.translate(x), self.consume, self.release, self.delay)  #! O(1)

    def scale(self, x: int, scale_release = True):
        """
        scales a rule

        Complexity: `O(1)`
        """
        _release = self.release * x if scale_release else self.release
        return Rule(self.rule_re.scale(x), self.consume * x, _release, self.delay)  #! O(1)


    #! Dunder Methods
    def __str__(self) -> str:
        return str(self.to_xmp_str())

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Rule):
            return self.rule_re == __o.rule_re and self.consume == __o.consume and self.release == __o.release and self.delay == __o.delay
        
        return False
    
    def __hash__(self):
        return hash((frozenset(self.rule_re), self.consume, self.release, self.delay))




    