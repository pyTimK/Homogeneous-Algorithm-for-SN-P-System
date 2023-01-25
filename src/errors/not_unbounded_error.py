class NotUnboundedError(Exception):
    """Raised when the input is not a finite union of unbounded regular expressions"""
    def __init__(self, type: int, reg_exp: str, unb_reg_exp: str):
        if (type == 0):
            message = "The algorithm does not work on bounded regular expressions in the form a^i"
        else:
            message = "The algorithm does not work on regular expressions with multiple stars, e.g., \"(2a)*(3a)*\""

        self.message = f"{message}\nThe error was found on \"{unb_reg_exp}\" part of the regular expression \"{reg_exp}\""

    def __str__(self):
        return self.message