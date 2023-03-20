class MultipleStarsError(Exception):
    """Raised when the input regular expression contains multiple stars"""
    def __init__(self, reg_exp: str, unb_reg_exp: str):
        message = "The algorithm does not work on regular expressions with multiple stars, e.g., \"(2a)*(3a)*\""
        self.message = f"{message}\nThe error was found on \"{unb_reg_exp}\" part of the regular expression \"{reg_exp}\""

    def __str__(self):
        return self.message