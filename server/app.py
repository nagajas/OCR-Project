from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import cv2
import io
import numpy as np
from PIL import Image

app = Flask(__name__)
CORS(app)

# Load model
model_path = 'models/mjsynth'
model = tf.keras.models.load_model(model_path)

# Mapping
characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
index_to_char = {idx: char for idx, char in enumerate(characters, start=0)}
unk_index = len(index_to_char)
index_to_char[unk_index] = 'UNK'

def preprocess_image(img):
    img = cv2.resize(img, (128, 32)) 
    img = img / 255.0 
    img = np.expand_dims(img, axis=-1) 
    return img

def decode_prediction(prediction):
    decoded_text = []
    for i in range(prediction.shape[1]):
        max_index = np.argmax(prediction[0][i])
        if max_index != unk_index:
            decoded_text.append(index_to_char.get(max_index, ''))
    return ''.join(decoded_text)

def make_prediction(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = preprocess_image(img)
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)
    decoded_text = decode_prediction(prediction)

    return decoded_text


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400
    
    file = request.files['image']
    
    try:
        image = Image.open(io.BytesIO(file.read()))
        img = np.array(image)
        extracted_text = make_prediction(img)
        
        return jsonify({'text': extracted_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
