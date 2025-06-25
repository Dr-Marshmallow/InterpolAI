import os
import uuid
from flask import Blueprint, render_template, request, jsonify, current_app, send_from_directory
from .models.super_resolution import process_image_for_upscaling
import base64
import cv2
import numpy as np
from PIL import Image
import io

main = Blueprint('main', __name__)

# Percorso assoluto per la cartella uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Create upload folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        ext = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Save the file
        file.save(file_path)
        
        return jsonify({
            "success": True,
            "filename": unique_filename,
            "filepath": f"/static/uploads/{unique_filename}"
        })
    
    return jsonify({"error": "File type not allowed"}), 400

@main.route('/enhance', methods=['POST'])
def enhance_image():
    data = request.json
    if not data or 'image_data' not in data or 'x' not in data or 'y' not in data or 'zoom_level' not in data:
        return jsonify({"error": "Missing required data"}), 400
    
    try:
        # Get coordinates and zoom level
        x = int(data['x'])
        y = int(data['y'])
        zoom_level = float(data['zoom_level'])
        
        # Get optional image adjustment parameters
        brightness = int(data.get('brightness', 0))
        contrast = int(data.get('contrast', 0))
        sharpness = int(data.get('sharpness', 0))
        saturation = int(data.get('saturation', 0))
        
        # Get image data from base64
        encoded_data = data['image_data'].split(',')[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Process the image for super-resolution
        enhanced_img = process_image_for_upscaling(
            img, 
            x, 
            y, 
            zoom_level,
            brightness=brightness,
            contrast=contrast,
            sharpness=sharpness,
            saturation=saturation
        )
        
        # Convert back to base64
        _, buffer = cv2.imencode('.png', enhanced_img)
        enhanced_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            "success": True,
            "enhanced_image": f"data:image/png;base64,{enhanced_base64}"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename) 