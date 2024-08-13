from flask import Flask, render_template, request
import cv2
from google.colab.patches import cv2_imshow
import numpy as np

app = Flask(__name__)

def perform_segmentation(image_path):
      # Load the image
      image = cv2.imread(image_path)

      # Convert to grayscale
      gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

      # Thresholding
      _, segmented_image = cv2.threshold(gray_image, 120, 255, cv2.THRESH_BINARY)

      # Morphological operations
      kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
      segmented_image = cv2.morphologyEx(segmented_image, cv2.MORPH_CLOSE, kernel)

      return segmented_image

@app.route('/', methods=['GET', 'POST'])
def index():
      if request.method == 'POST':
            # Check if the POST request has the file part
            if 'file' not in request.files:
                  return render_template('index.html', error='No file part')

            file = request.files['file']

            # Check if the file is empty
            if file.filename == '':
                  return render_template('index.html', error='No selected file')

            # Check if the file is an image
            if file and file.filename.endswith(('.jpg', '.jpeg', '.png')):
                  # Save the file to a temporary location
                  file_path = '/tmp/' + file.filename
                  file.save(file_path)

                  # Perform segmentation
                  segmented_image = perform_segmentation(file_path)

                  # Display the result
                  cv2_imshow(segmented_image)

                  return render_template('index.html', success=True)
            else:
                  return render_template('index.html', error='Invalid file format')

      return render_template('index.html')

if __name__ == '__main__':
      app.run(debug=True)
