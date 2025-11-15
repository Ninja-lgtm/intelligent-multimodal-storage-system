"""
Intelligent Multi-Modal Storage System
College Project Backend using Flask

This application automatically detects and stores different types of data:
- Images → storage/images/
- Videos → storage/videos/
- JSON → storage/json_data/ (with SQL/NoSQL classification)

Author: Kumar Amityush
Date: November 2025
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import send_from_directory

# Initialize Flask application
app = Flask(__name__)

# Enable CORS to allow frontend requests from different origins
CORS(app)

# Configuration: Define storage paths
STORAGE_BASE = 'storage'
IMAGE_FOLDER = os.path.join(STORAGE_BASE, 'images')
VIDEO_FOLDER = os.path.join(STORAGE_BASE, 'videos')
JSON_FOLDER = os.path.join(STORAGE_BASE, 'json_data')

# Allowed file extensions for validation
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'svg'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv', 'webm'}


def create_storage_folders():
    """
    Create storage folders if they don't exist.
    This ensures the application can store files without errors.
    """
    folders = [IMAGE_FOLDER, VIDEO_FOLDER, JSON_FOLDER]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"✓ Created folder: {folder}")


def allowed_file(filename, file_type):
    """
    Check if the uploaded file has an allowed extension.
    
    Args:
        filename (str): Name of the uploaded file
        file_type (str): Type of file ('image' or 'video')
    
    Returns:
        bool: True if extension is allowed, False otherwise
    """
    if '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    
    if file_type == 'image':
        return extension in ALLOWED_IMAGE_EXTENSIONS
    elif file_type == 'video':
        return extension in ALLOWED_VIDEO_EXTENSIONS
    
    return False


def classify_json_storage(json_data):
    """
    Analyze JSON structure to determine if it needs SQL or NoSQL storage.
    
    Logic:
    - If any value is a nested object (dict) OR list → NoSQL
    - If all values are simple types (string, number, boolean, null) → SQL
    
    Args:
        json_data (dict): Parsed JSON data
    
    Returns:
        str: 'nosql' or 'sql'
    """
    # Recursive function to check for complex structures
    def has_complex_structure(data):
        if isinstance(data, dict):
            # Check if any value in the dictionary is complex
            for value in data.values():
                if isinstance(value, (dict, list)):
                    return True
                if has_complex_structure(value):
                    return True
        elif isinstance(data, list):
            # Lists indicate NoSQL structure
            return True
        return False
    
    # Perform the classification
    if has_complex_structure(json_data):
        return 'nosql'
    else:
        return 'sql'


@app.route('/upload', methods=['POST'])
def upload():
    """
    Main upload endpoint that handles:
    1. Image files
    2. Video files
    3. JSON structured data
    
    Returns:
        JSON response with classification and storage information
    """
    try:
        # Extract optional comment/metadata
        comment = request.form.get('comment', '').strip()
        
        # Check if a file was uploaded
        if 'file' in request.files:
            file = request.files['file']
            
            # Validate that file is not empty
            if file.filename == '':
                return jsonify({
                    'error': 'No file selected',
                    'message': 'Please select a file to upload.'
                }), 400
            
            # Get MIME type of the uploaded file
            mime_type = file.content_type
            
            # Detect and process IMAGE files
            if mime_type.startswith('image/'):
                if not allowed_file(file.filename, 'image'):
                    return jsonify({
                        'error': 'Invalid image format',
                        'message': f'Allowed formats: {", ".join(ALLOWED_IMAGE_EXTENSIONS)}'
                    }), 400
                
                # Generate secure filename with timestamp to avoid conflicts
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = secure_filename(file.filename)
                unique_filename = f"{timestamp}_{filename}"
                filepath = os.path.join(IMAGE_FOLDER, unique_filename)
                
                # Save the image file
                file.save(filepath)
                
                return jsonify({
                    'input_type': 'image',
                    'chosen_storage': 'images',
                    'comment_received': comment if comment else '',
                    'filename': unique_filename,
                    'message': f'Image file successfully stored in images folder. The file was identified as an image based on its MIME type ({mime_type}) and saved with a timestamp to prevent naming conflicts.'
                }), 200
            
            # Detect and process VIDEO files
            elif mime_type.startswith('video/'):
                if not allowed_file(file.filename, 'video'):
                    return jsonify({
                        'error': 'Invalid video format',
                        'message': f'Allowed formats: {", ".join(ALLOWED_VIDEO_EXTENSIONS)}'
                    }), 400
                
                # Generate secure filename with timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = secure_filename(file.filename)
                unique_filename = f"{timestamp}_{filename}"
                filepath = os.path.join(VIDEO_FOLDER, unique_filename)
                
                # Save the video file
                file.save(filepath)
                
                return jsonify({
                    'input_type': 'video',
                    'chosen_storage': 'videos',
                    'comment_received': comment if comment else '',
                    'filename': unique_filename,
                    'message': f'Video file successfully stored in videos folder. The file was identified as a video based on its MIME type ({mime_type}) and saved with a timestamp to prevent naming conflicts.'
                }), 200
            
            else:
                return jsonify({
                    'error': 'Unsupported file type',
                    'message': f'The system only accepts image or video files. Received MIME type: {mime_type}'
                }), 400
        
        # Check if JSON data was provided via textarea
        elif 'json_data' in request.form:
            json_string = request.form.get('json_data', '').strip()
            
            if not json_string:
                return jsonify({
                    'error': 'Empty JSON data',
                    'message': 'Please provide valid JSON content in the textarea.'
                }), 400
            
            try:
                # Parse the JSON string
                parsed_json = json.loads(json_string)
                
                # Classify storage type (SQL vs NoSQL)
                storage_type = classify_json_storage(parsed_json)
                
                # Generate unique filename for JSON
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                json_filename = f"data_{timestamp}.json"
                json_filepath = os.path.join(JSON_FOLDER, json_filename)
                
                # Save JSON to file with pretty formatting
                with open(json_filepath, 'w', encoding='utf-8') as json_file:
                    json.dump(parsed_json, json_file, indent=2, ensure_ascii=False)
                
                # Create detailed explanation message
                if storage_type == 'nosql':
                    explanation = 'The JSON data contains nested objects or arrays, which require a flexible NoSQL database (like MongoDB) for optimal storage and querying. NoSQL databases handle complex, hierarchical data structures efficiently.'
                else:
                    explanation = 'The JSON data contains only simple key-value pairs with primitive types (strings, numbers, booleans). This can be efficiently stored in a traditional SQL database with a flat table structure.'
                
                return jsonify({
                    'input_type': 'json',
                    'chosen_storage': storage_type,
                    'comment_received': comment if comment else '',
                    'filename': json_filename,
                    'message': f'JSON data successfully parsed and saved. Classification: {storage_type.upper()}. {explanation}'
                }), 200
            
            except json.JSONDecodeError as e:
                return jsonify({
                    'error': 'Invalid JSON format',
                    'message': f'The provided JSON data is malformed. Error: {str(e)}'
                }), 400
        
        else:
            return jsonify({
                'error': 'No input provided',
                'message': 'Please provide either a file (image/video) or JSON data in the textarea.'
            }), 400
    
    except Exception as e:
        # Catch any unexpected errors
        return jsonify({
            'error': 'Internal server error',
            'message': f'An unexpected error occurred: {str(e)}'
        }), 500


@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint to verify the server is running.
    """
    return jsonify({
        'project': 'Intelligent Multi-Modal Storage System',
        'status': 'running',
        'endpoints': {
            'upload': '/upload (POST)',
            'methods': 'multipart/form-data'
        },
        'supported_inputs': ['images', 'videos', 'json_data'],
        'message': 'Server is ready to accept uploads!'
    }), 200


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify storage folders exist.
    """
    folders_status = {
        'images': os.path.exists(IMAGE_FOLDER),
        'videos': os.path.exists(VIDEO_FOLDER),
        'json_data': os.path.exists(JSON_FOLDER)
    }
    
    return jsonify({
        'status': 'healthy',
        'storage_folders': folders_status
    }), 200

@app.route('/retrieve', methods=['GET'])
def retrieve_data():
    result = {
        'images': os.listdir(IMAGE_FOLDER),
        'videos': os.listdir(VIDEO_FOLDER),
        'json_data': os.listdir(JSON_FOLDER)
    }
    return jsonify(result), 200


@app.route('/storage/<path:folder>/<path:filename>')
def serve_file(folder, filename):
    """
    Serve uploaded files from storage folders
    Allows frontend to view/download stored files
    """
    try:
        folder_path = os.path.join(STORAGE_BASE, folder)
        return send_from_directory(folder_path, filename)
    except FileNotFoundError:
        return jsonify({
            'error': 'File not found',
            'message': f'The requested file does not exist: {filename}'
        }), 404



if __name__ == '__main__':
    # Create storage folders on startup
    print("=" * 50)
    print("Intelligent Multi-Modal Storage System")
    print("=" * 50)
    create_storage_folders()
    print("\n✓ Server initialization complete!")
    print("✓ Endpoint: POST /upload")
    print("✓ Listening on: http://127.0.0.1:5000")
    print("=" * 50)
    
    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)