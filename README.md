# Universal Batch Image Downloader

![Python](https://img.shields.io/badge/Python-3-blue.svg) ![License](https://img.shields.io/badge/License-MIT-green.svg)

A powerful, general-purpose Python utility to batch download images from any URL pattern, resize them, and apply uniform padding/centering. Perfect for creating standardized assets for dashboards, games, or UI projects.

## Features

- **🖥️ Modern GUI**: Includes a user-friendly Desktop App (`gui_app.py`) built with `customtkinter`.
- **🎨 Smart Auto-Padding**: Automatically resizes images to fit within a specific bounding box while maintaining aspect ratio, then centers them on a unified canvas.
- **🚀 Batch Processing**: Download hundreds of images in seconds.
- **🔧 Universal Config**: Capable of grabbing tech logos, game sprites, country flags, or any web asset with a predictable URL structure.
- **🛡️ Error Handling**: Skips broken links gracefully without crashing.

## Quick Start

1.  **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

    _Note: This now includes `customtkinter` for the GUI._

2.  **Run the Application**:

    **Option A: GUI App (Recommended)**

    ```bash
    python gui_app.py
    ```

    - Paste your list of items.
    - Click "Start Download".

    **Option B: CLI Script**

    ```bash
    python downloader.py
    ```

    - Edit `downloader.py` directly to configure URL patterns and items list.

3.  **Check Output**:
    Images will appear in the `downloaded_assets` folder (or whatever you configured).

## Configuration Guide (CLI)

Open `downloader.py` and edit the **USER CONFIGURATION SECTION** at the top.

### Scenario A: Downloading Tech Logos

Use the Dashboard Icons CDN (default).

```python
URL_PATTERN = "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/png/{name}.png"
ITEMS_TO_DOWNLOAD = ["ubuntu-linux", "python", "docker", "react"]
```

### Scenario B: Downloading Pokemon Sprites

Use the PokeAPI repository.

```python
# Note: PokeAPI uses IDs or Names. '1' is Bulbasaur.
URL_PATTERN = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{name}.png"
ITEMS_TO_DOWNLOAD = ["1", "4", "7", "25", "150"] # Bulbasaur, Charmander, Squirtle, Pikachu, Mewtwo
```

### Scenario C: Downloading Country Flags

Use FlagCDN (uses 2-letter ISO codes).

```python
URL_PATTERN = "https://flagcdn.com/w320/{name}.png"
ITEMS_TO_DOWNLOAD = ["us", "gb", "fr", "jp", "de"]
```

## Customizing Dimensions

You can control the output look by adjusting these variables in `downloader.py` (or `gui_app.py` source):

- `CANVAS_SIZE`: The total size of the final image (e.g., 350x350).
- `IMAGE_MAX_SIZE`: The max size of the logo/sprite itself (e.g., 250x250).
- `PADDING_COLOR`: Background color (default is transparent).

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)
