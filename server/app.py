from flask import Flask, request, jsonify
from flask_cors import CORS
import easyocr
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'])  # You can add more languages if needed

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400
    
    file = request.files['image']
    
    try:
        # Open the image using PIL
        img = Image.open(io.BytesIO(file.read()))

        # Convert the image to bytes and then use EasyOCR to extract text
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=img.format)
        img_byte_arr = img_byte_arr.getvalue()

        result = reader.readtext(img_byte_arr)

        # Extract and concatenate all the detected text
        extracted_text = " ".join([text[1] for text in result])

        return jsonify({'text': extracted_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
