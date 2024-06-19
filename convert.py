import os
import glob

from PIL import Image, ImageDraw, ImageFont
import pytesseract

# Location with original RMIs
BASE_IMAGE_DIRECTORY = "/Users/ariessunfeld/Documents/LANL/main/msl/ccam/tools/clustering/cluster_graphs_and_zmaps/wrapin_RMI_mosaics_M100_merged_uptosol1162"

# Location where you want corrected RMIs to appear
OUTPUT_DIRECTORY = "/Users/ariessunfeld/Desktop/output_rescaled/"

# List of target names to convert (e.g., 'Ashuanipi', 'Yampi', etc
TARGETS_TO_CONVERT = [
    'Mell',
    # Add more targets here as needed
]

# Scale factor (multiplied by 300 dpi; default is 3)
SCALE = 3 

# Define the function to process the scalebar
def fix_scalebar(image_path):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    # Define the scalebar area (bottom right 130x60 pixels)
    scalebar_area = (image.width - 130, image.height - 60, image.width, image.height)
    scalebar_image = image.crop(scalebar_area)
    
    # Use OCR to extract the text (mm value) from the scalebar area
    scalebar_text = pytesseract.image_to_string(scalebar_image, config='--psm 6').strip()

    mode = None
    
    if 'mm' in scalebar_text:
        # Extract the numeric value from the text (e.g., "5.5 mm" -> 5.5)
        try:
            scalebar_value = float(scalebar_text.split('mm')[0])
            mode = 'mm'
        except ValueError:
            
            print(f"Could not extract scalebar value from text: {scalebar_text}")
            return image
    elif 'cm' in scalebar_text:
         # Extract the numeric value from the text (e.g., "5.5 mm" -> 5.5)
        try:
            scalebar_value = 10 * float(scalebar_text.split('cm')[0])
            mode = 'cm'
        except ValueError:
            
            print(f"Could not extract scalebar value from text: {scalebar_text}")
            return image

    else:
        print(f"Could not extract scalebar value from text: {scalebar_text}")
        return image
            
    # Calculate the scale factor (1 cm = 10 mm)
    scale_factor = 10 / scalebar_value if mode == 'mm' else 20 / scalebar_value

    # set a rectangle radius in pixels
    rect_radius = 6

    # set an amount that the endcap sticks out
    endcap_diff = 8

    # set the width of the endcap
    endcap_width = 8
    
    # Draw the new scalebar (100 pixels wide, positioned 10 pixels from the bottom)
    new_scalebar_length = int(106 * scale_factor)
    new_scalebar_start_x = image.width - new_scalebar_length - 20
    new_scalebar_start_y = image.height - 10 - 10
    new_scalebar_end_x = new_scalebar_start_x + new_scalebar_length
    new_scalebar_end_y = new_scalebar_start_y

    # Draw a black rectangle to cover the old scalebar
    draw.rectangle([image.width-130, image.height-60, image.width, image.height], fill='black')
    
    # Draw a white rectangle to overwrite the old scalebar
    draw.rectangle([new_scalebar_start_x, new_scalebar_start_y - rect_radius, new_scalebar_end_x, new_scalebar_start_y + rect_radius], fill="white")

    # Draw white endcap to left of scalebar
    draw.rectangle([
        new_scalebar_start_x,
        new_scalebar_start_y - rect_radius - endcap_diff,
        new_scalebar_start_x + endcap_width,
        new_scalebar_start_y + rect_radius + endcap_diff],
        fill='white')

    draw.rectangle([
        new_scalebar_end_x - endcap_width,
        new_scalebar_start_y - rect_radius - endcap_diff,
        new_scalebar_end_x,
        new_scalebar_start_y + rect_radius + endcap_diff],
        fill='white')
    
    # Draw the new scalebar text
    font = ImageFont.truetype("Arial.ttf", 64)  # Use a suitable font and size
    text_position = (new_scalebar_end_x-120, new_scalebar_start_y-90)
    draw.text(text_position, "1cm" if mode == 'mm' else '2cm', fill="white", font=font)
    
    return image


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
    for target in TARGETS_TO_CONVERT:
        pattern = os.path.join(BASE_IMAGE_DIRECTORY, f"*{target}_after*")
        files = glob.glob(pattern)
        first = files[0]
        fname = first.split(os.sep)[-1]
        fname_stem = fname.split('.png')[0]
        corrected = fix_scalebar(first)
        corrected.save(os.path.join(OUTPUT_DIRECTORY, f'{fname_stem}_corrected.png'))
    
