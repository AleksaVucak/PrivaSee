import cv2
import os

def map_blur_level_to_kernel(blur_level, max_kernel_size=101):
    """
    Maps a blur level from 0 to 100 to an appropriate Gaussian kernel size.
    The kernel size will range from 1 (no blur) to max_kernel_size (maximum blur).
    """
    if max_kernel_size % 2 == 0:
        max_kernel_size += 1

    if blur_level == 0:
        return 1  # No blur
    kernel_size = int((blur_level / 100) * (max_kernel_size - 1)) + 1
    return kernel_size if kernel_size % 2 != 0 else kernel_size + 1

def blur_image(image_path, blur_level):
    """
    Blurs an image using a Gaussian Blur with the specified blur level.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Cannot open image: {image_path}")
    
    kernel_size = map_blur_level_to_kernel(blur_level)
    blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    return blurred_image

def process_dataset(dataset_dir, blur_levels):
    """
    Blurs all images in a dataset directory by a range of blur levels and saves them.
    """
    # Define the output folder for blurred images
    blur_results_folder = os.path.join(os.path.expanduser("~"), "Desktop", "BLUR RESULTS")
    os.makedirs(blur_results_folder, exist_ok=True)
    
    for filename in os.listdir(dataset_dir):
        file_path = os.path.join(dataset_dir, filename)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp', '.avif')):
            for blur_level in blur_levels:
                try:
                    blurred_image = blur_image(file_path, blur_level)
                    base_name, ext = os.path.splitext(filename)
                    new_filename = f"{base_name}_blur{blur_level}{ext}"
                    new_file_path = os.path.join(blur_results_folder, new_filename)
                    cv2.imwrite(new_file_path, blurred_image)
                    print(f"Saved {new_file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

# Define the path to the dataset folder on your desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
dataset_dir = os.path.join(desktop_path, "Initial DS")

# Define the blur levels to apply
blur_levels = [0, 15, 30, 45, 60, 75, 100]

# Process the dataset
process_dataset(dataset_dir, blur_levels)
