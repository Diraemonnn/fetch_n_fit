import os
import requests
import io
from PIL import Image

# ==========================================
#        USER CONFIGURATION SECTION
# ==========================================

# 1. URL Pattern
# Use {name} as a placeholder for the item name.
# Example 1 (Tech Icons): "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/png/{name}.png"
# Example 2 (Pokemon): "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{name}.png" (Use ID numbers for names)
URL_PATTERN = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{name}.png"

# 2. Items to Download
# Valid names dependent on the source URL.
ITEMS_TO_DOWNLOAD = [
    "1", # Bulbasaur
    "4", # Charmander
    "7", # Squirtle
    "25" # Pikachu
]

# 3. Output Settings
OUTPUT_FOLDER = "downloaded_assets"

# 4. Image Processing Settings
# The size of the transparent background canvas
CANVAS_SIZE = (350, 350) 

# The maximum size of the downloaded image inside the canvas
# It will be resized to fit within this box while maintaining aspect ratio.
# Making this smaller than CANVAS_SIZE creates padding/breathing room.
IMAGE_MAX_SIZE = (250, 250)

# Background color (R, G, B, A). (0,0,0,0) is fully transparent.
PADDING_COLOR = (0, 0, 0, 0) 


# ==========================================
#              CORE LOGIC
#      (Do not modify below this line)
# ==========================================

def download_image(name):
    """Downloads image from URL_PATTERN."""
    url = URL_PATTERN.format(name=name)
    try:
        print(f"Fetching {name} from {url}...")
        headers = {'User-Agent': 'UniversalBatchDownloader/1.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
        else:
            print(f"  [ERROR] Failed with status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"  [ERROR] Connection failed: {e}")
        return None

def process_and_save(img, name, output_dir):
    """Resizes, centers, and saves the image."""
    try:
        # Ensure RGBA for transparency support
        img = img.convert("RGBA")
        
        # 1. Resize logic (Maintain Aspect Ratio)
        width, height = img.size
        ratio = min(IMAGE_MAX_SIZE[0] / width, IMAGE_MAX_SIZE[1] / height)
        new_size = (int(width * ratio), int(height * ratio))
        
        # High-quality downscaling
        img_resized = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # 2. Canvas creation
        canvas = Image.new("RGBA", CANVAS_SIZE, PADDING_COLOR)
        
        # 3. Centering logic
        x_pos = (CANVAS_SIZE[0] - new_size[0]) // 2
        y_pos = (CANVAS_SIZE[1] - new_size[1]) // 2
        
        canvas.paste(img_resized, (x_pos, y_pos), img_resized)
        
        # 4. Saving
        save_path = os.path.join(output_dir, f"{name}.png")
        canvas.save(save_path, "PNG")
        print(f"  [SUCCESS] Saved to {save_path}")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Processing failed for {name}: {e}")
        return False

def main():
    print("--- Universal Batch Image Downloader Started ---")
    
    # Create output directory
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"Created output folder: {OUTPUT_FOLDER}")
    
    success_count = 0
    fail_count = 0
    
    for item in ITEMS_TO_DOWNLOAD:
        img = download_image(item)
        
        if img:
            if process_and_save(img, item, OUTPUT_FOLDER):
                success_count += 1
            else:
                fail_count += 1
        else:
            fail_count += 1
            
    print("\n--- Download Summary ---")
    print(f"Total: {len(ITEMS_TO_DOWNLOAD)}")
    print(f"Success: {success_count}")
    print(f"Failed: {fail_count}")

if __name__ == "__main__":
    main()
