"""
Intelligent Multi-Modal Storage System with User Authentication
College Project Backend using Flask

Features:
- User Registration & Login
- Session Management
- Per-user Storage Isolation
- Secure Password Hashing

Author: Kumar Amityush
Date: November 2025
"""

from flask import Flask, request, jsonify, send_from_directory, send_file, session
from flask_cors import CORS
import os
import json
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets
import mimetypes

# Initialize Flask application
app = Flask(__name__)

# Secret key for session management
app.secret_key = secrets.token_hex(32)

# UPDATED: More comprehensive CORS configuration
CORS(app, 
     supports_credentials=True,
     resources={
         r"/*": {
             "origins": [
                 "http://127.0.0.1:8000",
                 "http://localhost:8000",
                 "http://127.0.0.1:5500",
                 "http://localhost:5500",
                 "null"  # For file:// protocol
             ],
             "allow_headers": ["Content-Type", "Authorization"],
             "expose_headers": ["Content-Type"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "supports_credentials": True,
             "max_age": 3600
         }
     }
)
# Configuration: Define storage paths
STORAGE_BASE = 'storage'
USERS_DB = os.path.join(STORAGE_BASE, 'users.json')

# Allowed file extensions for validation
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'svg'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv', 'webm'}
ALLOWED_PDF_EXTENSIONS = {'pdf'}


def create_storage_folders():
    """
    Create storage folders if they don't exist.
    """
    if not os.path.exists(STORAGE_BASE):
        os.makedirs(STORAGE_BASE)
        print(f"✓ Created folder: {STORAGE_BASE}")
    
    # Create users database if it doesn't exist
    if not os.path.exists(USERS_DB):
        with open(USERS_DB, 'w') as f:
            json.dump({}, f)
        print(f"✓ Created users database")


def get_user_storage_path(username, subfolder):
    """
    Get storage path for a specific user
    """
    user_folder = os.path.join(STORAGE_BASE, username, subfolder)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    return user_folder


def load_users():
    """
    Load users from JSON database
    """
    try:
        with open(USERS_DB, 'r') as f:
            return json.load(f)
    except:
        return {}


def save_users(users_data):
    """
    Save users to JSON database
    """
    with open(USERS_DB, 'w') as f:
        json.dump(users_data, f, indent=2)


def require_login(f):
    """
    Decorator to require login for protected routes
    """
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Please login to access this resource'
            }), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


def allowed_file(filename, file_type):
    """
    Check if the uploaded file has an allowed extension.
    """
    if '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    
    if file_type == 'image':
        return extension in ALLOWED_IMAGE_EXTENSIONS
    elif file_type == 'video':
        return extension in ALLOWED_VIDEO_EXTENSIONS
    elif file_type == 'pdf':
        return extension in ALLOWED_PDF_EXTENSIONS
    
    return False


def detect_file_type(filename):
    """
    Auto-detect file type based on extension.
    Returns: 'image', 'video', 'pdf', or None
    """
    if '.' not in filename:
        return None
    
    extension = filename.rsplit('.', 1)[1].lower()
    
    if extension in ALLOWED_IMAGE_EXTENSIONS:
        return 'image'
    elif extension in ALLOWED_VIDEO_EXTENSIONS:
        return 'video'
    elif extension in ALLOWED_PDF_EXTENSIONS:
        return 'pdf'
    
    return None


def classify_json_storage(json_data):
    """
    Analyze JSON structure to determine if it needs SQL or NoSQL storage.
    """
    def has_complex_structure(data):
        if isinstance(data, dict):
            for value in data.values():
                if isinstance(value, (dict, list)):
                    return True
                if has_complex_structure(value):
                    return True
        elif isinstance(data, list):
            return True
        return False
    
    if has_complex_structure(json_data):
        return 'nosql'
    else:
        return 'sql'


# ==================== AUTHENTICATION ROUTES ====================

@app.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    """
    try:
        data = request.get_json()
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        email = data.get('email', '').strip()
        full_name = data.get('full_name', '').strip()
        
        # Validation
        if not username or not password or not email:
            return jsonify({
                'error': 'Missing required fields',
                'message': 'Username, password, and email are required'
            }), 400
        
        if len(username) < 3:
            return jsonify({
                'error': 'Invalid username',
                'message': 'Username must be at least 3 characters long'
            }), 400
        
        if len(password) < 6:
            return jsonify({
                'error': 'Weak password',
                'message': 'Password must be at least 6 characters long'
            }), 400
        
        # Load existing users
        users = load_users()
        
        # Check if username already exists
        if username in users:
            return jsonify({
                'error': 'Username taken',
                'message': 'This username is already registered'
            }), 409
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        # Create user record
        users[username] = {
            'password': hashed_password,
            'email': email,
            'full_name': full_name,
            'created_at': datetime.now().isoformat(),
            'uploads': {
                'images': [],
                'videos': [],
                'json_data': []
            }
        }
        
        # Save to database
        save_users(users)
        
        # Create user storage folders
        get_user_storage_path(username, 'images')
        get_user_storage_path(username, 'videos')
        get_user_storage_path(username, 'json_data')
        
        return jsonify({
            'success': True,
            'message': 'Registration successful! Please login.',
            'username': username
        }), 201
    
    except Exception as e:
        return jsonify({
            'error': 'Registration failed',
            'message': str(e)
        }), 500


@app.route('/login', methods=['POST'])
def login():
    """
    Login user and create session
    """
    try:
        data = request.get_json()
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({
                'error': 'Missing credentials',
                'message': 'Username and password are required'
            }), 400
        
        # Load users
        users = load_users()
        
        # Check if user exists
        if username not in users:
            return jsonify({
                'error': 'Invalid credentials',
                'message': 'Username or password is incorrect'
            }), 401
        
        # Verify password
        if not check_password_hash(users[username]['password'], password):
            return jsonify({
                'error': 'Invalid credentials',
                'message': 'Username or password is incorrect'
            }), 401
        
        # Create session
        session['username'] = username
        session['email'] = users[username]['email']
        session['full_name'] = users[username].get('full_name', username)
        
        return jsonify({
            'success': True,
            'message': 'Login successful!',
            'user': {
                'username': username,
                'email': users[username]['email'],
                'full_name': users[username].get('full_name', username)
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': 'Login failed',
            'message': str(e)
        }), 500


@app.route('/logout', methods=['POST'])
def logout():
    """
    Logout user and clear session
    """
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    }), 200


@app.route('/check-session', methods=['GET'])
def check_session():
    """
    Check if user is logged in
    """
    if 'username' in session:
        return jsonify({
            'logged_in': True,
            'user': {
                'username': session['username'],
                'email': session.get('email', ''),
                'full_name': session.get('full_name', session['username'])
            }
        }), 200
    else:
        return jsonify({
            'logged_in': False
        }), 200


# ==================== PROTECTED ROUTES ====================

@app.route('/upload', methods=['POST'])
@require_login
def upload():
    """
    Upload endpoint - now requires authentication
    """
    try:
        username = session['username']
        comment = request.form.get('comment', '').strip()
        
        # Load user data
        users = load_users()
        
        if 'file' in request.files:
            file = request.files['file']
            
            if file.filename == '':
                return jsonify({
                    'error': 'No file selected',
                    'message': 'Please select a file to upload.'
                }), 400
            
            mime_type = file.content_type
            
            # Handle IMAGE files
            if mime_type.startswith('image/'):
                if not allowed_file(file.filename, 'image'):
                    return jsonify({
                        'error': 'Invalid image format',
                        'message': f'Allowed formats: {", ".join(ALLOWED_IMAGE_EXTENSIONS)}'
                    }), 400
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = secure_filename(file.filename)
                unique_filename = f"{timestamp}_{filename}"
                
                folder = get_user_storage_path(username, 'images')
                filepath = os.path.join(folder, unique_filename)
                file.save(filepath)
                
                # Update user record
                users[username]['uploads']['images'].append({
                    'filename': unique_filename,
                    'comment': comment,
                    'uploaded_at': datetime.now().isoformat()
                })
                save_users(users)
                
                return jsonify({
                    'input_type': 'image',
                    'chosen_storage': 'images',
                    'comment_received': comment if comment else '',
                    'filename': unique_filename,
                    'message': f'Image uploaded successfully to your personal storage.'
                }), 200
            
            # Handle VIDEO files
            elif mime_type.startswith('video/'):
                if not allowed_file(file.filename, 'video'):
                    return jsonify({
                        'error': 'Invalid video format',
                        'message': f'Allowed formats: {", ".join(ALLOWED_VIDEO_EXTENSIONS)}'
                    }), 400
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = secure_filename(file.filename)
                unique_filename = f"{timestamp}_{filename}"
                
                folder = get_user_storage_path(username, 'videos')
                filepath = os.path.join(folder, unique_filename)
                file.save(filepath)
                
                # Update user record
                users[username]['uploads']['videos'].append({
                    'filename': unique_filename,
                    'comment': comment,
                    'uploaded_at': datetime.now().isoformat()
                })
                save_users(users)
                
                return jsonify({
                    'input_type': 'video',
                    'chosen_storage': 'videos',
                    'comment_received': comment if comment else '',
                    'filename': unique_filename,
                    'message': f'Video uploaded successfully to your personal storage.'
                }), 200
            
            # Handle PDF files
            elif mime_type == 'application/pdf' or file.filename.lower().endswith('.pdf'):
                if not allowed_file(file.filename, 'pdf'):
                    return jsonify({
                        'error': 'Invalid PDF format',
                        'message': 'Only PDF files are accepted.'
                    }), 400
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = secure_filename(file.filename)
                unique_filename = f"{timestamp}_{filename}"
                
                folder = get_user_storage_path(username, 'pdfs')
                filepath = os.path.join(folder, unique_filename)
                file.save(filepath)
                
                # Update user record
                if 'pdfs' not in users[username]['uploads']:
                    users[username]['uploads']['pdfs'] = []
                users[username]['uploads']['pdfs'].append({
                    'filename': unique_filename,
                    'comment': comment,
                    'uploaded_at': datetime.now().isoformat()
                })
                save_users(users)
                
                return jsonify({
                    'input_type': 'pdf',
                    'chosen_storage': 'pdfs',
                    'comment_received': comment if comment else '',
                    'filename': unique_filename,
                    'message': f'PDF uploaded successfully to your personal storage.'
                }), 200
            
            else:
                return jsonify({
                    'error': 'Unsupported file type',
                    'message': f'Supported: images, videos, and PDFs. Received: {mime_type}'
                }), 400
        
        # Handle JSON data
        elif 'json_data' in request.form:
            json_string = request.form.get('json_data', '').strip()
            
            if not json_string:
                return jsonify({
                    'error': 'Empty JSON data',
                    'message': 'Please provide valid JSON content.'
                }), 400
            
            try:
                parsed_json = json.loads(json_string)
                storage_type = classify_json_storage(parsed_json)
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                json_filename = f"data_{timestamp}.json"
                
                folder = get_user_storage_path(username, 'json_data')
                json_filepath = os.path.join(folder, json_filename)
                
                with open(json_filepath, 'w', encoding='utf-8') as json_file:
                    json.dump(parsed_json, json_file, indent=2, ensure_ascii=False)
                
                # Update user record
                users[username]['uploads']['json_data'].append({
                    'filename': json_filename,
                    'storage_type': storage_type,
                    'comment': comment,
                    'uploaded_at': datetime.now().isoformat()
                })
                save_users(users)
                
                if storage_type == 'nosql':
                    explanation = 'NoSQL classification: Contains nested objects or arrays.'
                else:
                    explanation = 'SQL classification: Simple key-value pairs only.'
                
                return jsonify({
                    'input_type': 'json',
                    'chosen_storage': storage_type,
                    'comment_received': comment if comment else '',
                    'filename': json_filename,
                    'message': f'JSON data saved successfully. {explanation}'
                }), 200
            
            except json.JSONDecodeError as e:
                return jsonify({
                    'error': 'Invalid JSON format',
                    'message': f'Malformed JSON: {str(e)}'
                }), 400
        
        else:
            return jsonify({
                'error': 'No input provided',
                'message': 'Please provide a file or JSON data.'
            }), 400
    
    except Exception as e:
        return jsonify({
            'error': 'Upload failed',
            'message': str(e)
        }), 500


@app.route('/retrieve', methods=['GET'])
@require_login
def retrieve_data():
    """
    Retrieve user's uploaded files
    """
    try:
        username = session['username']
        
        images_folder = get_user_storage_path(username, 'images')
        videos_folder = get_user_storage_path(username, 'videos')
        json_folder = get_user_storage_path(username, 'json_data')
        pdfs_folder = get_user_storage_path(username, 'pdfs')
        
        result = {
            'images': os.listdir(images_folder) if os.path.exists(images_folder) else [],
            'videos': os.listdir(videos_folder) if os.path.exists(videos_folder) else [],
            'json_data': os.listdir(json_folder) if os.path.exists(json_folder) else [],
            'pdfs': os.listdir(pdfs_folder) if os.path.exists(pdfs_folder) else []
        }
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            'error': 'Retrieval failed',
            'message': str(e)
        }), 500

@app.route('/public/<path:username>/<path:folder>/<path:filename>', methods=['GET'])
def serve_public_file(username, folder, filename):
    folder_path = os.path.abspath(os.path.join(STORAGE_BASE, username, folder))
    if not folder_path.startswith(os.path.abspath(STORAGE_BASE)):
        return jsonify({'error': 'Invalid path'}), 400
    if not os.path.exists(folder_path):
        return jsonify({'error': 'Folder not found'}), 404
    return send_from_directory(folder_path, filename)

@app.route('/storage/<path:username>/<path:folder>/<path:filename>')
@require_login
def serve_file(username, folder, filename):
    """
    Serve user's uploaded files (with authorization check)
    """
    try:
        # Check if user is accessing their own files
        if session['username'] != username:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'You can only access your own files'
            }), 403
        
        # Validate folder path
        if folder not in ['images', 'videos', 'json_data', 'pdfs']:
            return jsonify({
                'error': 'Invalid folder',
                'message': 'Invalid storage folder'
            }), 400
        
        # Build the full file path
        folder_path = os.path.join(STORAGE_BASE, username, folder)
        file_path = os.path.join(folder_path, filename)
        
        # Normalize paths to prevent directory traversal
        folder_path = os.path.abspath(folder_path)
        file_path = os.path.abspath(file_path)
        
        # Ensure file is within the storage folder
        if not file_path.startswith(folder_path):
            return jsonify({
                'error': 'Invalid path',
                'message': 'Access denied'
            }), 403
        
        # Check if file exists
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return jsonify({
                'error': 'File not found',
                'message': f'The file {filename} does not exist'
            }), 404
        
        # Serve the file directly using send_file
        mimetype = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
        return send_file(file_path, mimetype=mimetype, as_attachment=False)
    
    except Exception as e:
        print(f"Error serving file {filename}: {str(e)}")
        return jsonify({
            'error': 'Server error',
            'message': f'Failed to serve file: {str(e)}'
        }), 500


@app.route('/download/<path:username>/<path:folder>/<path:filename>')
@require_login
def download_file(username, folder, filename):
    """
    Download user's uploaded files (with authorization check and force download)
    """
    try:
        # Check if user is accessing their own files
        if session['username'] != username:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'You can only access your own files'
            }), 403
        
        # Validate folder
        if folder not in ['images', 'videos', 'json_data', 'pdfs']:
            return jsonify({
                'error': 'Invalid folder',
                'message': 'Invalid storage folder'
            }), 400
        
        # Build the full file path
        folder_path = os.path.join(STORAGE_BASE, username, folder)
        file_path = os.path.join(folder_path, filename)
        
        # Normalize paths to prevent directory traversal
        folder_path = os.path.abspath(folder_path)
        file_path = os.path.abspath(file_path)
        
        # Ensure file is within the storage folder
        if not file_path.startswith(folder_path):
            return jsonify({
                'error': 'Invalid path',
                'message': 'Access denied'
            }), 403
        
        # Check if file exists
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return jsonify({
                'error': 'File not found',
                'message': f'The file {filename} does not exist'
            }), 404
        
        # Download the file using send_file
        mimetype = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
        return send_file(
            file_path,
            mimetype=mimetype,
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        print(f"Error downloading file {filename}: {str(e)}")
        return jsonify({
            'error': 'Download failed',
            'message': str(e)
        }), 500


@app.route('/dashboard-stats', methods=['GET'])
@require_login
def dashboard_stats():
    """
    Get user's dashboard statistics
    """
    try:
        username = session['username']
        users = load_users()
        
        user_data = users.get(username, {})
        uploads = user_data.get('uploads', {})
        
        stats = {
            'total_images': len(uploads.get('images', [])),
            'total_videos': len(uploads.get('videos', [])),
            'total_pdfs': len(uploads.get('pdfs', [])),
            'total_json': len(uploads.get('json_data', [])),
            'recent_uploads': []
        }
        
        # Get recent uploads (last 5)
        all_uploads = []
        for img in uploads.get('images', []):
            all_uploads.append({**img, 'type': 'image'})
        for vid in uploads.get('videos', []):
            all_uploads.append({**vid, 'type': 'video'})
        for pdf in uploads.get('pdfs', []):
            all_uploads.append({**pdf, 'type': 'pdf'})
        for js in uploads.get('json_data', []):
            all_uploads.append({**js, 'type': 'json'})
        
        # Sort by upload time
        all_uploads.sort(key=lambda x: x.get('uploaded_at', ''), reverse=True)
        stats['recent_uploads'] = all_uploads[:5]
        
        return jsonify(stats), 200
    
    except Exception as e:
        return jsonify({
            'error': 'Failed to load stats',
            'message': str(e)
        }), 500


# ==================== PUBLIC ROUTES ====================

@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint
    """
    return jsonify({
        'project': 'Intelligent Multi-Modal Storage System',
        'version': '2.0 with Authentication',
        'status': 'running',
        'endpoints': {
            'register': '/register (POST)',
            'login': '/login (POST)',
            'logout': '/logout (POST)',
            'upload': '/upload (POST) - Requires Auth',
            'retrieve': '/retrieve (GET) - Requires Auth'
        }
    }), 200


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }), 200


if __name__ == '__main__':
    print("=" * 50)
    print("Intelligent Multi-Modal Storage System v2.0")
    print("With User Authentication")
    print("=" * 50)
    create_storage_folders()
    print("\n✓ Server initialization complete!")
    print("✓ Authentication enabled")
    print("✓ Listening on: http://127.0.0.1:5000")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)