import os
import csv
import numpy as np
from PIL import Image
from Centroid_kaar import get_centroids_from_image

# --- CONFIGURATION ---
# Use 'r' before the quotes to avoid the SyntaxWarning
IMAGE_PATH = "Photos/Starry.jpeg" 
# ---------------------

def run_single_file():
    # 1. Check if file exists
    if not os.path.exists(IMAGE_PATH):
        print(f"Error: The file '{IMAGE_PATH}' was not found!")
        print("Check if the 'Photos' folder is inside your current directory.")
        return

    print(f"Processing: {IMAGE_PATH}")

    try:
        # 2. Load and convert to Grayscale
        img = Image.open(IMAGE_PATH).convert('L')
        img_array = np.array(img)

        # 3. Extract centroids (using logic from Centroid_kaar.py)
        # We use sigma=3 to filter noise
        centroids = get_centroids_from_image(img_array, sigma=3)

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

    except Exception as e:
        print(f"  [ERROR] Something went wrong: {e}")

if __name__ == "__main__":
    run_single_file()