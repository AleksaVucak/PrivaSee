import os
import pandas as pd

def extract_blur_level(file_name):
    parts = file_name.split('_')
    if len(parts) > 1:
        blur_part = parts[1]
        # Extract numeric value from blur_part (e.g., "blur30" -> 30)
        blur_level = ''.join(filter(str.isdigit, blur_part))
        return blur_level
    return None

def extract_return_value(file_name):
    parts = file_name.split('_')
    if len(parts) > 2:
        number = parts[-1].split('.')
        return_value = float(number[0] + '.' + number[1]) 
        try:
            return str(return_value)  
        except ValueError:
            return None  
    return None

def map_return_values(folder_path, data, column_name):
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist. Skipping...")
        return

    files = [file_name for file_name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file_name))]
    for row in data:
        for file_name in files:
            parts = file_name.split('_')
            if len(parts) > 2 and parts[0] == row["File Name"] and f"blur{row['Blur Level']}" == parts[1]:
                row[column_name] = extract_return_value(file_name)
                break

def create_csv(desktop_path):
    blur_results_path = os.path.join(desktop_path, "blur results")
    r1_path = os.path.join(desktop_path, "R1")
    r3_path = os.path.join(desktop_path, "R3")
    r4_path = os.path.join(desktop_path, "R4")
    output_csv_path = os.path.join(desktop_path, "output.csv")
    if not os.path.exists(blur_results_path):
        print(f"Folder {blur_results_path} does not exist.")
        return
    file_names = sorted(
        [file_name for file_name in os.listdir(blur_results_path) if os.path.isfile(os.path.join(blur_results_path, file_name))]
    )
    data = []
    for file_name in file_names:
        blur_level = extract_blur_level(file_name)
        data.append({
            "File Name": file_name.split('_')[0],  
            "Blur Type": "Gaussian",
            "Blur Level": blur_level,
            "OpenCV Return Value": None,
            "FFT Return Value": None,
            "Tenengrad Gradient Return Value": None
        })

    map_return_values(r1_path, data, "OpenCV Return Value")
    map_return_values(r3_path, data, "FFT Return Value")
    map_return_values(r4_path, data, "Tenengrad Gradient Return Value")
    df = pd.DataFrame(data)
    df.to_csv(output_csv_path, index=False)
    print(f"CSV file created successfully at: {output_csv_path}")

# Define the desktop path
desktop_path = os.path.expanduser("~/Desktop")

# Create the CSV file
create_csv(desktop_path)