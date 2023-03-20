class NotBoundedError(Exception):
    """Raised when the Period Constant Pair is not bounded"""
    def __init__(self):
        self.message = "The Period Constant Pair is not bounded"

    def __str__(self):
        return self.message