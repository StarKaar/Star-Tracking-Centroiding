from c_interface import get_centroids_fast
from PIL import Image
import numpy as np
import os
import csv

IMAGE_PATH = "Photos/newlife.jpeg"

img = Image.open(IMAGE_PATH).convert('L')
img_array = np.array(img)

# Use the ultra-fast C version
centroids = get_centroids_fast(img_array, threshold=60, win_size=7)

# ... save to CSV exactly as you did before ...
if centroids is not None and len(centroids) > 0:
    # 4. Create the CSV filename
    base = os.path.splitext(IMAGE_PATH)[0]
    csv_name = f"{base}_centroids.csv"
            
    with open(csv_name, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['x', 'y'])
        writer.writeheader()
        # Important: Centroid_kaar returns (y, x), cenplot wants (x, y)
        for (y, x) in centroids:
            writer.writerow({'x': x, 'y': y})
    
    print(f"  [SUCCESS] Found {len(centroids)} stars.")
    print(f"  [SUCCESS] Saved data to: {csv_name}")
else:
    print("  [INFO] No stars detected in this image.")

