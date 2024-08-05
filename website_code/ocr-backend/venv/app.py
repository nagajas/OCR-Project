from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import pytesseract
import io
import base64

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    image = Image.open(file.stream)
    
    # Perform OCR
    text = pytesseract.image_to_string(image)
    
    # For demonstration, we return the original image as base64
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return jsonify({'outputImage': img_str})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
