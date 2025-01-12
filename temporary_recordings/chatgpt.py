import json
import struct
from PIL import Image

def float_to_bytes_little_endian(value):
    """Convert a float64 to 8 bytes in little-endian format."""
    return struct.pack('<d', value)

def create_frame_data_image(json_file, output_png):
    # Step 1: Read JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Step 2: Extract frame_data
    frame_data = data.get("frame_data", [])
    if not isinstance(frame_data, list):
        raise ValueError("frame_data must be a list.")
    
    # Step 3: Create a blank RGBA image
    width = len(frame_data)  # One column per frame_data element
    height = 4  # Fixed height (4 pixels high)
    img = Image.new("RGBA", (width, height))
    pixels = img.load()

    # Step 4: Process each element in frame_data
    for x, (num1, num2) in enumerate(frame_data):
        # Convert both floats to 8-byte little-endian representations
        bytes1 = float_to_bytes_little_endian(num1)
        bytes2 = float_to_bytes_little_endian(num2)

        # Write bytes for the first number (num1) into the first two rows (2 pixels)
        pixels[x, 0] = tuple(bytes1[:4])  # First pixel (RGBA: bytes 0-3)
        pixels[x, 1] = tuple(bytes1[4:])  # Second pixel (RGBA: bytes 4-7)

        # Write bytes for the second number (num2) into the next two rows (2 pixels)
        pixels[x, 2] = tuple(bytes2[:4])  # Third pixel (RGBA: bytes 0-3)
        pixels[x, 3] = tuple(bytes2[4:])  # Fourth pixel (RGBA: bytes 4-7)

    # Step 5: Save the image
    #img.save(output_png, pnginfo=None, optimize=True)
    img.save(output_png[:-4]+".webp", format='WEBP', lossless=True)
    print(f"Image saved as {output_png}")

# Example usage
json_file = "spirally_thing.json"  # Replace with your JSON file path
output_png = "spirally_thing.png"
create_frame_data_image(json_file, output_png)
