# WEEK 6

def karatsuba(u: int, v: int) -> int:
    """
    Multiply two non-negative integers using Karatsuba algorithm (binary-based).
    """
    # Base case: small numbers multiply directly
    if -2 < u < 2 or -2 < v < 2:
        return u * v

    n = max(u.bit_length(), v.bit_length())
    d = n // 2 # split the bits in half according to the max split

    u1, u0 = u >> d   ,   u & ((1 << d) - 1)
    v1, v0 = v >> d   ,   v & ((1 << d) - 1)

    diff_u = u1 - u0
    diff_v = v1 - v0
    
    z0 = karatsuba(u0, v0)
    z1 = karatsuba(diff_u, diff_v)
    z2 = karatsuba(u1, v1)  

    # Combination of the three products
    return (
         ((z2 << (d << 1)) + (z2 << d)) # (2^2d + 2^d) * U1 * V1
        - (z1 << d)                     # 2^d * (U1 − U0) * (V1 − V0)
        + (z0 << d) + z0                # (2^d + 1) * U0 * V0
    )

def karatsuba_test(a, b):
    c = karatsuba(a, b)
    d = a * b
    print(f"{a} × {b} =", c)
    print("Expected:", d)
    print(f"Same? {c == d}")
    
if __name__ == "__main__":
    karatsuba_test(561, 123456789)