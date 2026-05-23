# ComfyUI-FakeEXIF

A custom node for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) that allows you to save generated images while **completely removing all ComfyUI and AI metadata (prompts, workflow, etc.)**. Instead, it injects fake EXIF metadata to make the image appear as if it was taken by a real smartphone.

## Features
- **100% Metadata wipe**: No AI traces left in the saved image.
- **Custom GPS Coordinates**: Define latitude and longitude.
- **Custom Camera Model**: Defaults to Apple iPhone 16 Pro Max.
- **Automatic Datetime**: Automatically captures the exact real-time generation date and time.
- **Realistic formatting**: Simulates iOS software metadata out of the box.

## Installation

### Method 1: ComfyUI Manager
(If available in the manager)
1. Search for `Fake EXIF` or `ComfyUI-FakeEXIF`.
2. Click Install and restart ComfyUI.

### Method 2: Manual
1. Navigate to your ComfyUI `custom_nodes` folder.
2. Clone this repository:
   ```bash
   git clone https://github.com/Bigornh2o/ComfyUI-FakeEXIF.git
   ```
3. Navigate into the folder and install the requirement (`piexif`):
   ```bash
   cd ComfyUI-FakeEXIF
   pip install -r requirements.txt
   ```
4. Restart ComfyUI.

## Usage
Simply replace your standard `Save Image` node with the **Save Image (Fake EXIF)** node located in the `image` category. 

Set your GPS coordinates, choose your format (JPG is highly recommended for best EXIF support), and generate!
