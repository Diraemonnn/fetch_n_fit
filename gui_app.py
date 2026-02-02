import customtkinter as ctk
import threading
import requests
import io
import os
from PIL import Image

# Constants from original script
CANVAS_SIZE = (350, 350)
IMAGE_MAX_SIZE = (250, 250)
PADDING_COLOR = (0, 0, 0, 0)

class BatchDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Universal Batch Downloader")
        self.geometry("600x700")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("dark-blue")

        # Grid Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=0)  # URL Input
        self.grid_rowconfigure(2, weight=1)  # Textbox (expandable)
        self.grid_rowconfigure(3, weight=0)  # Button & Progress

        # --- Top Section ---
        self.header_label = ctk.CTkLabel(
            self, 
            text="Universal Batch Downloader", 
            font=("Roboto", 24, "bold")
        )
        self.header_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        # --- Middle Section ---
        
        # URL Pattern Input
        self.url_label = ctk.CTkLabel(self, text="URL Pattern ({name} is placeholder):")
        self.url_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")

        self.url_entry = ctk.CTkEntry(self, placeholder_text="Enter URL pattern...")
        self.url_entry.grid(row=2, column=0, padx=20, pady=(5, 10), sticky="ew")
        # Pre-fill with Devicon URL as requested
        self.url_entry.insert(0, "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/png/{name}.png")

        # Items Textbox
        self.items_label = ctk.CTkLabel(self, text="Items to Download (One per line):")
        self.items_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")

        self.items_textbox = ctk.CTkTextbox(self, height=300)
        self.items_textbox.grid(row=4, column=0, padx=20, pady=(5, 10), sticky="nsew")

        # --- Bottom Section ---

        # Start Button
        self.start_button = ctk.CTkButton(
            self, 
            text="Start Download", 
            command=self.start_download_thread,
            font=("Roboto", 16, "bold"),
            height=40
        )
        self.start_button.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.grid(row=6, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.progress_bar.set(0)

        # Status Label
        self.status_label = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.status_label.grid(row=7, column=0, padx=20, pady=(0, 20), sticky="ew")

    def start_download_thread(self):
        """Starts the download process in a separate thread."""
        url_pattern = self.url_entry.get()
        raw_items = self.items_textbox.get("1.0", "end")
        
        # Parse items (split by newline and remove empty strings)
        items = [line.strip() for line in raw_items.splitlines() if line.strip()]

        if not items:
            self.status_label.configure(text="Error: No items to download!", text_color="red")
            return

        # Disable UI during download
        self.start_button.configure(state="disabled")
        self.items_textbox.configure(state="disabled")
        self.url_entry.configure(state="disabled")
        
        # Start Thread
        threading.Thread(target=self.run_download_process, args=(url_pattern, items), daemon=True).start()

    def run_download_process(self, url_pattern, items):
        """Background thread logic for downloading and processing images."""
        output_folder = "downloaded_assets"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        total_items = len(items)
        success_count = 0
        
        for idx, item in enumerate(items):
            # Update UI (Status & Progress) from thread
            progress = (idx / total_items)
            self.after(0, self.update_status, f"Downloading {item}...", progress)
            
            try:
                # 1. Download
                url = url_pattern.format(name=item)
                headers = {'User-Agent': 'UniversalBatchDownloader/1.0'}
                response = requests.get(url, headers=headers, timeout=10)

                if response.status_code == 200:
                    img = Image.open(io.BytesIO(response.content))
                    
                    # 2. Process & Save
                    if self.process_and_save(img, item, output_folder):
                        success_count += 1
                else:
                    print(f"Failed to download {item}: Status {response.status_code}")
            
            except Exception as e:
                print(f"Error downloading {item}: {e}")

        # Finish
        self.after(0, self.finish_process, success_count, total_items)

    def process_and_save(self, img, name, output_dir):
        """Resizes, centers, and saves the image."""
        try:
            img = img.convert("RGBA")
            
            # Resize
            width, height = img.size
            ratio = min(IMAGE_MAX_SIZE[0] / width, IMAGE_MAX_SIZE[1] / height)
            new_size = (int(width * ratio), int(height * ratio))
            img_resized = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Canvas
            canvas = Image.new("RGBA", CANVAS_SIZE, PADDING_COLOR)
            
            # Center
            x_pos = (CANVAS_SIZE[0] - new_size[0]) // 2
            y_pos = (CANVAS_SIZE[1] - new_size[1]) // 2
            
            canvas.paste(img_resized, (x_pos, y_pos), img_resized)
            
            # Save
            save_path = os.path.join(output_dir, f"{name}.png")
            canvas.save(save_path, "PNG")
            return True
        except Exception as e:
            print(f"Processing failed for {name}: {e}")
            return False

    def update_status(self, message, progress):
        """Updates the status label and progress bar safely."""
        self.status_label.configure(text=message, text_color="white")
        self.progress_bar.set(progress)

    def finish_process(self, success_count, total_items):
        """Restores UI state after download completes."""
        self.progress_bar.set(1.0)
        self.status_label.configure(text=f"Done! ({success_count}/{total_items} successful)", text_color="green")
        
        # Re-enable UI
        self.start_button.configure(state="normal")
        self.items_textbox.configure(state="normal")
        self.url_entry.configure(state="normal")

if __name__ == "__main__":
    app = BatchDownloaderApp()
    app.mainloop()
