import cv2
import os

def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

def blur_detection(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_level = variance_of_laplacian(gray)
    return blur_level

def process_images(folder_path):
    desktop = os.path.expanduser("~/Desktop")
    output_folder = os.path.join(desktop, "R1")
    os.makedirs(output_folder, exist_ok=True)
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if not os.path.isfile(file_path):
            continue
        blur_level = blur_detection(file_path)
        image = cv2.imread(file_path)
        file_base, file_ext = os.path.splitext(filename)
        new_filename = f"{file_base}_{blur_level:.2f}{file_ext}"
        new_file_path = os.path.join(output_folder, new_filename)
        cv2.imwrite(new_file_path, image)

def main():
    desktop = os.path.expanduser("~/Desktop")
    input_folder_name = "blur results"
    input_folder_path = os.path.join(desktop, input_folder_name)
    
    if not os.path.exists(input_folder_path):
        print(f"Folder '{input_folder_name}' not found on your desktop.")
        return
    
    process_images(input_folder_path)
    print("Processing complete. Check the 'R1' folder on your desktop.")

if __name__ == "__main__":
    main()
