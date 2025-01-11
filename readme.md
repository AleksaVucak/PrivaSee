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
