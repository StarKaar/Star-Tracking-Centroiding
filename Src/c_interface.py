import ctypes
import numpy as np
import os

# 1. Define the structure to match the C code
class StarCentroid(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float),
                ("y", ctypes.c_float),
                ("flux", ctypes.c_float)]

# 2. Load the DLL
import ctypes
import numpy as np
import os

# 1. Define the structure
class StarCentroid(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float),
                ("y", ctypes.c_float),
                ("flux", ctypes.c_float)]

# 2. LOAD THE DLL (Smart Pathing)
# This gets the folder where c_interface.py is actually located
current_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(current_dir, "centroid.dll")

if not os.path.exists(lib_path):
    raise FileNotFoundError(f"Could not find centroid.dll at {lib_path}")

# On Windows, we need to specify winmode=0 for some Python versions
try:
    centroid_lib = ctypes.CDLL(lib_path)
except Exception as e:
    # If the standard load fails, try the Windows-specific safe load
    centroid_lib = ctypes.PyDLL(lib_path)

# 3. Setup the function arguments
centroid_lib.find_star_centroids.argtypes = [
    ctypes.POINTER(ctypes.c_uint8), # image
    ctypes.c_int,                  # width
    ctypes.c_int,                  # height
    ctypes.c_uint8,                # threshold
    ctypes.c_int,                  # win_size
    ctypes.POINTER(StarCentroid),  # results array
    ctypes.c_int                   # max_stars
]
centroid_lib.find_star_centroids.restype = ctypes.c_int

def get_centroids_fast(image_array, threshold=50, win_size=5):
    h, w = image_array.shape
    max_stars = 100000  # Set a very high limit to avoid truncation, adjust as needed
    # Create an array of structures to hold results
    results = (StarCentroid * max_stars)()
    
    # Call the C function
    count = centroid_lib.find_star_centroids(
        image_array.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),
        w, h, threshold, win_size, results, max_stars
    )
    
    # Convert results back to a Python list of (y, x) to match your existing scripts
    return [(results[i].y, results[i].x) for i in range(count)]