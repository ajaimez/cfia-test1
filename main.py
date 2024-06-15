from flask import Flask, flash, request, redirect, url_for, render_template
from markupsafe import Markup
import urllib.request
import os
from werkzeug.utils import secure_filename

# import cv2  # OpenCV for image processing
# import matplotlib.pyplot as plt  # Matplotlib for visualization
import numpy as np  # NumPy for numerical operations
import easyocr  # EasyOCR for text extraction from images
 
app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        clave = OCRProces(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')

        flash(Markup('<b>DATO: ' + clave + '</b>'))
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


def OCRProces(image_path):
    # Reading the image
    # image = cv2.imread(image_path)

    # Initializing the EasyOCR reader with English language support and GPU disabled
    reader = easyocr.Reader(['es'], gpu=False)

    # Extracting text from the image
    results = reader.readtext(image_path)

    # Displaying the extracted results
    for detection in results:
        # if detection[1].startswith('Clave'): #or detection[1].startswith('506') :
        #     print(detection[1])
        #     break
        if 'Clave' in detection[1] or ('506' in detection[1] and len(detection[1])>30):
            print(detection[1])
            clave = detection[1]
            break
    return clave    
 
if __name__ == "__main__":
    app.run()