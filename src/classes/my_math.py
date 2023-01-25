import math

class MyMath:
    @staticmethod
    def lcm(a: int, b: int):
        return (a*b)//math.gcd(a,b)