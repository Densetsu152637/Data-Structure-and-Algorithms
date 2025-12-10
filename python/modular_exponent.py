# WEEK 6

def mod_exp(base: int, exp: int, mod: int) -> int:
    """
    Modular exponentiation using repeated squaring.
    Computes (base^exp) % mod efficiently.
    """
    result = 1
    base = base % mod
    while exp > 0:
        if exp & 1: # If exponent is odd
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result