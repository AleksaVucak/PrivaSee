import cv2
import numpy as np
import os

def detect_blur_fft(image_path, threshold=10):
    """Detect if an image is blurry using the FFT method."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"Could not open or find the image: {image_path}")
        return
    
    # Compute the FFT and shift zero frequency component to the center
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift))

    # Calculate the mean magnitude spectrum
    mean_magnitude = np.mean(magnitude_spectrum)

    return mean_magnitude

def process_images(input_folder, output_folder, threshold=10):
    """Process all images in the folder and save with updated filenames."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if not os.path.isfile(file_path):
            continue
        
        # Run FFT blur detection
        blur_level = detect_blur_fft(file_path, threshold)
        
        # Construct the new filename: original filename + _<variance>.ext
        file_base, file_ext = os.path.splitext(filename)
        new_filename = f"{file_base}_{blur_level:.2f}{file_ext}"
        output_path = os.path.join(output_folder, new_filename)
        
        # Copy the original image to the new file with the updated name
        image = cv2.imread(file_path)
        cv2.imwrite(output_path, image)
        print(f"Processed and saved: {output_path}")

# Define input and output folders
input_folder = os.path.expanduser("~/Desktop/blur results")
output_folder = os.path.expanduser("~/Desktop/R3")

# Run the processing function on all images in the input folder
process_images(input_folder, output_folder)