import cv2
import numpy as np
import os

def detect_blur_tenengrad(image_path, threshold=500):
    """Detect if an image is blurry using the Tenengrad/Sobel method."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"Could not open or find the image: {image_path}")
        return None, None, None
    
    # Calculate the Sobel gradients
    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

    # Calculate the mean of the gradient magnitude
    mean_gradient_magnitude = np.mean(gradient_magnitude)
    is_blurry = mean_gradient_magnitude < threshold
    return is_blurry, mean_gradient_magnitude, cv2.imread(image_path)

def process_images(input_folder, output_folder, threshold=500):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        image_path = os.path.join(input_folder, filename)
        is_blurry, mean_gradient_magnitude, color_image = detect_blur_tenengrad(image_path, threshold)
        
        if color_image is not None:
            # Create the new filename with only the variance appended
            file_base, file_ext = os.path.splitext(filename)
            new_filename = f"{file_base}_{mean_gradient_magnitude:.2f}{file_ext}"
            output_path = os.path.join(output_folder, new_filename)

            # Save the processed image without any overlay
            cv2.imwrite(output_path, color_image)
            print(f"Processed and saved: {output_path}")

# Define input and output paths
desktop_path = os.path.expanduser("~/Desktop")
input_folder = os.path.join(desktop_path, "blur results")
output_folder = os.path.join(desktop_path, "R4")

# Process all images in the input folder
process_images(input_folder, output_folder)