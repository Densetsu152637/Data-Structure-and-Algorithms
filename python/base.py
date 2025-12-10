
import importlib.util, subprocess, sys

def require_package(package: str):
    if importlib.util.find_spec(package) is None:
        print(f"Installing missing package: {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])     

def typeof(obj) -> str:
    return obj.__class__.__name__

def round_up_to_nearest_power_of_two(n: int):
    if n <= 0:
        raise ValueError("Input must be a positive integer.")
    
    # If n is already a power of two, return n
    if (n & (n - 1)) == 0:
        return n
    
    # Otherwise, find the next power of two
    # This works by finding the highest set bit and then shifting left by 1
    # For example, if n = 6 (binary 110), n.bit_length() is 3.
    # 1 << 3 gives 8 (binary 1000).
    return 1 << n.bit_length()