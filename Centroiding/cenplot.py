import csv
import argparse
from pathlib import Path
from PIL import Image, ImageDraw

# --- CONFIGURATION ---
DOT_SIZE = 5

def process_directory(directory_path):
    directory_path = Path(directory_path)

    # 1. Validation
    if not directory_path.is_dir():
        print(f"Error: The path '{directory_path}' is not a valid directory.")
        return

    print(f"--- [LOG] Scanning directory: {directory_path} ---")

    # 2. Find all CSV files
    csv_files = sorted(directory_path.glob("*.csv"))
    
    if not csv_files:
        print("  [INFO] No CSV files found.")
        return

    processed_count = 0

    for csv_path in csv_files:
        # 3. Determine matching image name
        # Assumption: "name_centroids.csv" matches "name.jpeg"
        # We try to remove "_centroids" from the stem if it exists
        stem_name = csv_path.stem
        if stem_name.endswith("_centroids"):
            image_stem = stem_name.replace("_centroids", "")
        else:
            # Fallback if naming convention isn't strict
            image_stem = stem_name

        # Look for the image with common extensions
        image_path = None
        for ext in ['.jpeg', '.jpg', '.png']:
            possible_path = directory_path / (image_stem + ext)
            if possible_path.exists():
                image_path = possible_path
                break
        
        # 4. Process the pair if image exists
        if image_path:
            print(f"--- [LOG] Pair Found: {csv_path.name} <-> {image_path.name} ---")
            plot_centroids_on_image(csv_path, image_path)
            processed_count += 1
        else:
            print(f"  [WARN] Skipping {csv_path.name}: No matching image found (looked for {image_stem}.jpeg/jpg/png)")

    print(f"--- [LOG] Batch complete. Processed {processed_count} pairs. ---")


def plot_centroids_on_image(csv_path, image_path):
    points = []

    try:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            
            # Check if file is empty
            if reader.fieldnames is None:
                print(f"  [SKIP] CSV is empty (0 bytes or no headers).")
                return

            # Check for required columns
            if 'x' not in reader.fieldnames or 'y' not in reader.fieldnames:
                print(f"  [SKIP] CSV missing 'x' or 'y' headers.")
                return

            for row in reader:
                try:
                    x = float(row['x'])
                    y = float(row['y'])
                    points.append((x, y))
                except ValueError:
                    continue
                    
    except Exception as e:
        print(f"  [ERROR] Could not read CSV: {e}")
        return

    if not points:
        print(f"  [INFO] No stars found in CSV file.")
        return

    # Open the Image
    try:
        img = Image.open(image_path).convert('RGB')
        draw = ImageDraw.Draw(img)

        # Draw Stars
        for (x, y) in points:
            r = DOT_SIZE / 2
            # Draw GREEN circle
            draw.ellipse([x - r, y - r, x + r, y + r], outline='green', width=2)

        # Save
        output_filename = image_path.stem + '_overlay.jpeg'
        output_path = image_path.parent / output_filename
        
        img.save(output_path)
        print(f"  [SUCCESS] Saved overlay to: {output_filename}")

    except Exception as e:
        print(f"  [ERROR] Image processing failed: {e}")

if __name__ == "__main__":
    # This tells cenplot to look inside the Photos folder for the image and CSV
    process_directory("Photos")