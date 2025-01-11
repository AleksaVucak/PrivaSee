# Personal Health Information Blur

## Face and Text detection

Patient information in healthcare is among the most sensitive types of data. This data
includes protected health information (PHI) such as patient names, medical records, test results,
and visual data found in healthcare settings. According to a 2022 report by the Department of
Health and Human Services, healthcare data breaches have risen by 15%, with over 42 million
patient records exposed. Cybercriminals exploit this data for identity theft, financial fraud, and
resale on the dark web.

This project addresses these concerns by exploring and implementing solutions to de-
identify PHI from visual data in healthcare settings. The objective is to evaluate, test, and deploy

various PHI detection models. This involves us using algorithms capable of detecting and
obscuring sensitive information such as faces and written text. A variety of open-source
algorithms work together in this project to detect and remove this PHI.
This project aims to implement effective de-identification techniques including text
detection algorithms (e.g., EasyOCR, CRAFT, PaddleOCR) and face detection algorithms to
ensure the end goal is achieved. Furthermore, our primary objective is to ensure that sensitive
information is fully obscured while preserving the usability of the data for operational and
research purposes. This project supports patient privacy and strengthens data security in
healthcare environments.

## Face Detection

### MTCNN
MTCNN (Multi-Task Cascaded Convolutional Networks) is a popular open-source model for face detection. It uses a three-stage process designed to accurately identify and detect faces within the data. Firstly, it scans an image to identify potential face regions and places boxes around areas that could be faces. Secondly, it refines these regions by filtering out false positives, i.e., areas that are not faces. Finally, it uses a 5-feature landmark to detect facial features such as the eyes, nose, and corners of the mouth. These steps ensure accurate and reliable detection, which ultimately ensures all PHI (faces) is obscured. 
<img width="692" alt="Screenshot 2025-01-10 at 11 37 00 PM" src="https://github.com/user-attachments/assets/24907ca2-f6ca-4ba5-a9dd-76a0e11ad3ab" />

### RetinaFace
RetinaFace is a facial detection and recognition model that uses a single-stage detector, unlike MTCNN’s three-stage detector. It identifies faces and key landmarks like the eyes, nose, and mouth. It performs well in challenging conditions, such as poor lighting or angled faces, making it suitable for detecting complex data in our project. According to the University of Jakarta, RetinaFace was tested on datasets like WiderFace, Essex Faces94, and Essex Faces95 to evaluate its accuracy and speed. Results showed average precision (AP) on the WiderFace dataset of 94.20% (easy), 93.24% (medium), and 83.55% (hard)
<img width="692" alt="Screenshot 2025-01-10 at 11 37 14 PM" src="https://github.com/user-attachments/assets/b5d28938-8516-4355-b482-267c58be78bd" />

### InsightFace
InsightFace is a face detection and recognition model known for its high accuracy and ability to detect facial landmarks, such as eyes, nose, and mouth. Unlike MTCNN and RetinaFace which uses a 5-feature landmark system, InsightFace uses a 108-feature landmark system which can detect the important section across various facial features. This detailed landmark detection ensures precise and reliable results, making it suitable for our project.
<img width="800" alt="Screenshot 2025-01-10 at 11 38 52 PM" src="https://github.com/user-attachments/assets/611a4440-26df-4994-8b9a-2b8a5c8a1e51" />

## Text Detection

### CRAFT
The CRAFT model (Character Region Awareness for Text detection) is designed to locate and identify text in images with high accuracy. It uses a unique thermal heat map approach to highlight areas where text is likely to be present. This method allows the model to detect individual characters and link them together to form complete words, making it effective for complex layouts or uneven text. Its accuracy and reliability made it a model that we used within our project.
<img width="700" alt="Screenshot 2025-01-10 at 11 37 26 PM" src="https://github.com/user-attachments/assets/8be0fecf-6e20-4274-a8ff-0e17109a32b1" />

### EasyOCR
EasyOCR is a lightweight optical character recognition (OCR) model that extracts text from images and videos. It supports over 80+ languages, some of which include English, German, French, and more. It works well even with unclear or handwritten text. It is powered by an OCR engine and outputs the confidence level of the detected text, as well as bounding boxes and the coordinates for those bounding.
<img width="900" alt="Screenshot 2025-01-10 at 11 45 52 PM" src="https://github.com/user-attachments/assets/2d5e5230-bc63-4a95-a4be-bd15ec4b06ab" />

### PaddleOCR
PaddleOCR is an advanced OCR model built using the PaddlePaddle library in Python. This model works particularly well for very small or hard-to-read text and supports a wide range of languages. PaddleOCR uses deep learning techniques to detect text regions and predict bounding boxes. This multi-step process is crucial for detecting PHI within our data to ensure de-identification of sensitive information. Its use in our project was essential for identifying bounding boxes around small text found on walls, wording on badges and signs that may have included sensitive information.
<img width="800" alt="Screenshot 2025-01-10 at 11 48 53 PM" src="https://github.com/user-attachments/assets/e159f7da-be04-4a82-a5de-8f877eaf713f" />

# Steps for Model Execution and Results Processing

## Step 1: Virtual Environment Setup
- Each model requires its own virtual environment, created using Python's `venv` (refer to the ReadMe for instructions on how to do this, along with downloading all dependencies).
- This ensures the isolation of dependencies, Python versions, and required packages for each model.
- After the virtual environment is created, the Python `subprocess` module is used to run the model's Python code, ensuring that the correct environment is used for execution.

---

## Step 2: Results Saving and Folder Structure
- **Text File Results**: After each model is run, the results from each model (face detection and text detection) are saved in separate `.txt` files within designated folders.
  - **Face Model Results**: Bounding boxes for detected faces are saved as regular rectangular boxes, defined by the coordinates for the top-left and bottom-right corners.
  - **Text Model Results**: Bounding boxes for detected text are saved as polygonal boxes, defined by four coordinates representing each corner. This format allows for irregularly shaped text regions, such as text in unusual positions or on curved surfaces, to be accurately captured.

---

## Step 3: Image Processing Functions
- **Blurring Shapes**: This function obscures sensitive areas (such as faces or text) by applying a blur effect to the corresponding bounding boxes found in the detection results.
- **Applying Bounding Boxes**: This function overlays the detected bounding boxes onto the original images to visually represent the results.
- **Image Workflow**:
  - Before processing, images should be moved to the appropriate results folder (face or text models).
  - The system reads the detection results from the `.txt` files, applies the bounding boxes and blurs to the images, and saves the final processed images back to the respective results folder.

---

## Step 4: Decision Layer
- A decision layer can be implemented before applying the bounding boxes to filter results based on confidence scores to improve the reliability of the output.
- This is used to refine or merge bounding boxes to improve clarity and accuracy, particularly in cases where multiple bounding boxes overlap or are too close together.


## Results
<img width="800" alt="Screenshot 2025-01-10 at 11 50 08 PM" src="https://github.com/user-attachments/assets/40611825-620b-42ae-9d25-4c50a482f29e" />

### Setup
Requires python versions **3.8.10** and **3.7.4**, and the following instructions are for Windows only

Each folder in the models directory requires a venv of it's own, since each model requires specific libraries to run, use the exact python.exe from the source folder to create venv's with correct python version. On Windows you can find this by running the following in command prompt.
``` 
where python 
```

for each model, cd into the corresponding folder and run 
```
[path_to_specific_version_python_exe] -m venv [venv_name] 
venv_name\Scripts\activate 
pip install --upgrade pip 
pip install -r requirements.txt
```

Follow this list when deciding which version of python to use for each model

3.8.10
- easyocr
- insightface
- mtcnn

3.7.4
- craft
- paddle_ocr
- retina_face

## Running the main.py

` python main.py [input folder] [output_folder] `

## Disclaimer
files in the craft folder are not mine, they are taken directly from the CRAFT text model repo, you can check them out at the link below.
[link to craft repo](https://github.com/clovaai/CRAFT-pytorch)
