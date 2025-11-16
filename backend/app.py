"""
Intelligent Multi-Modal Storage System with Minio Cloud Storage
College Project Backend using Flask

Features:
- User Registration & Login
- Session Management
- Per-user Storage Isolation
- Secure Password Hashing
- Minio Cloud Storage Integration

Author: Triple Threat
Date: November 2025
"""

from flask import Flask, request, jsonify, send_from_directory, session, send_file
from flask_cors import CORS
import os
import json
import mimetypes
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets
from database import JSONDatabaseManager
from minio import Minio
from minio.error import S3Error
from io import BytesIO

# Initialize Flask application
app = Flask(__name__)

# Secret key for session management
app.secret_key = secrets.token_hex(32)

# Enable CORS with credentials support
CORS(app, supports_credentials=True, origins=[
    "http://127.0.0.1:5500",
    "http://127.0.0.1:8000",
    "http://localhost:5500",
    "http://localhost:8000",
    "file://",
    "null"
])

# Configuration: Define storage paths
STORAGE_BASE = 'storage'
USERS_DB = os.path.join(STORAGE_BASE, 'users.json')

# Minio Configuration
MINIO_ENDPOINT = "play.min.io"  # Change to your Minio server
MINIO_ACCESS_KEY = "minioadmin"  # Change to your access key
MINIO_SECRET_KEY = "minioadmin"  # Change to your secret key
MINIO_BUCKET = "intelligent-storage"  # Your bucket name
MINIO_SECURE = True  # Use HTTPS

# Initialize Minio client
try:
    minio_client = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=MINIO_SECURE
    )
    
    # Create bucket if it doesn't exist
    if not minio_client.bucket_exists(MINIO_BUCKET):
        minio_client.make_bucket(MINIO_BUCKET)
        print(f"✓ Created Minio bucket: {MINIO_BUCKET}")
    else:
        print(f"✓ Minio bucket exists: {MINIO_BUCKET}")
    
    MINIO_ENABLED = True
    print("✓ Minio cloud storage initialized successfully!")
except Exception as e:
    print(f"⚠ Warning: Minio not available - {e}")
    print("⚠ Falling back to local storage")
    MINIO_ENABLED = False

# Ensure storage directory exists before initializing database
if not os.path.exists(STORAGE_BASE):
    os.makedirs(STORAGE_BASE)

# Initialize Database Manager
db_manager = JSONDatabaseManager(STORAGE_BASE)

# Allowed file extensions for validation
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'svg'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv', 'webm'}


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


def upload_to_minio(file_data, object_name, content_type):
    """
    Upload file to Minio cloud storage
    """
    if not MINIO_ENABLED:
        return False
    
    try:
        # Create a BytesIO object from file data
        file_stream = BytesIO(file_data)
        file_size = len(file_data)
        
        # Upload to Minio
        minio_client.put_object(
            MINIO_BUCKET,
            object_name,
            file_stream,
            file_size,
            content_type=content_type
        )
        return True
    except S3Error as e:
        print(f"Minio upload error: {e}")
        return False


def download_from_minio(object_name):
    """
    Download file from Minio cloud storage
    """
    if not MINIO_ENABLED:
        return None
    
    try:
        response = minio_client.get_object(MINIO_BUCKET, object_name)
        return response.read()
    except S3Error as e:
        print(f"Minio download error: {e}")
        return None


def delete_from_minio(object_name):
    """
    Delete file from Minio cloud storage
    """
    if not MINIO_ENABLED:
        return False
    
    try:
        minio_client.remove_object(MINIO_BUCKET, object_name)
        return True
    except S3Error as e:
        print(f"Minio delete error: {e}")
        return False


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
    
    return False


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
            'storage_location': 'minio' if MINIO_ENABLED else 'local',
            'uploads': {
                'images': [],
                'videos': [],
                'json_data': []
            }
        }
        
        # Save to database
        save_users(users)
        
        # Create user storage folders (local backup)
        get_user_storage_path(username, 'images')
        get_user_storage_path(username, 'videos')
        get_user_storage_path(username, 'json_data')
        
        return jsonify({
            'success': True,
            'message': 'Registration successful! Please login.',
            'username': username,
            'storage': 'Minio Cloud Storage' if MINIO_ENABLED else 'Local Storage'
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
                'full_name': users[username].get('full_name', username),
                'storage': 'Minio Cloud' if MINIO_ENABLED else 'Local'
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
    Upload endpoint with Minio cloud storage support
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
                
                # Read file data
                file_data = file.read()
                
                # Upload to Minio
                minio_path = f"{username}/images/{unique_filename}"
                if MINIO_ENABLED:
                    upload_to_minio(file_data, minio_path, mime_type)
                
                # Save locally as backup
                folder = get_user_storage_path(username, 'images')
                filepath = os.path.join(folder, unique_filename)
                with open(filepath, 'wb') as f:
                    f.write(file_data)
                
                # Update user record
                users[username]['uploads']['images'].append({
                    'filename': unique_filename,
                    'comment': comment,
                    'uploaded_at': datetime.now().isoformat(),
                    'storage': 'minio' if MINIO_ENABLED else 'local',
                    'minio_path': minio_path if MINIO_ENABLED else None
                })
                save_users(users)
                
                return jsonify({
                    'input_type': 'image',
                    'chosen_storage': 'images',
                    'comment_received': comment if comment else '',
                    'filename': unique_filename,
                    'storage_location': 'Minio Cloud' if MINIO_ENABLED else 'Local',
                    'message': f'Image uploaded successfully to {"Minio cloud storage" if MINIO_ENABLED else "local storage"}.'
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
                
                # Read file data
                file_data = file.read()
                
                # Upload to Minio
                minio_path = f"{username}/videos/{unique_filename}"
                if MINIO_ENABLED:
                    upload_to_minio(file_data, minio_path, mime_type)
                
                # Save locally as backup
                folder = get_user_storage_path(username, 'videos')
                filepath = os.path.join(folder, unique_filename)
                with open(filepath, 'wb') as f:
                    f.write(file_data)
                
                # Update user record
                users[username]['uploads']['videos'].append({
                    'filename': unique_filename,
                    'comment': comment,
                    'uploaded_at': datetime.now().isoformat(),
                    'storage': 'minio' if MINIO_ENABLED else 'local',
                    'minio_path': minio_path if MINIO_ENABLED else None
                })
                save_users(users)
                
                return jsonify({
                    'input_type': 'video',
                    'chosen_storage': 'videos',
                    'comment_received': comment if comment else '',
                    'filename': unique_filename,
                    'storage_location': 'Minio Cloud' if MINIO_ENABLED else 'Local',
                    'message': f'Video uploaded successfully to {"Minio cloud storage" if MINIO_ENABLED else "local storage"}.'
                }), 200
            
            else:
                return jsonify({
                    'error': 'Unsupported file type',
                    'message': f'Only images and videos are accepted. Received: {mime_type}'
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
                
                # Save to local file
                folder = get_user_storage_path(username, 'json_data')
                json_filepath = os.path.join(folder, json_filename)
                
                with open(json_filepath, 'w', encoding='utf-8') as json_file:
                    json.dump(parsed_json, json_file, indent=2, ensure_ascii=False)
                
                # Upload to Minio
                minio_path = f"{username}/json_data/{json_filename}"
                if MINIO_ENABLED:
                    json_bytes = json.dumps(parsed_json, indent=2).encode('utf-8')
                    upload_to_minio(json_bytes, minio_path, 'application/json')
                
                # Store in database
                entry_id = db_manager.store_json(
                    username=username,
                    filename=json_filename,
                    storage_type=storage_type,
                    json_data=parsed_json,
                    comment=comment
                )
                
                # Update user record
                users[username]['uploads']['json_data'].append({
                    'filename': json_filename,
                    'storage_type': storage_type,
                    'comment': comment,
                    'entry_id': entry_id,
                    'uploaded_at': datetime.now().isoformat(),
                    'storage': 'minio' if MINIO_ENABLED else 'local',
                    'minio_path': minio_path if MINIO_ENABLED else None
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
                    'storage_location': 'Minio Cloud' if MINIO_ENABLED else 'Local',
                    'message': f'JSON data saved successfully to {"Minio cloud storage" if MINIO_ENABLED else "local storage"}. {explanation}'
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
        
        result = {
            'images': os.listdir(images_folder) if os.path.exists(images_folder) else [],
            'videos': os.listdir(videos_folder) if os.path.exists(videos_folder) else [],
            'json_data': os.listdir(json_folder) if os.path.exists(json_folder) else [],
            'storage_info': {
                'enabled': MINIO_ENABLED,
                'type': 'Minio Cloud Storage' if MINIO_ENABLED else 'Local Storage'
            }
        }
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            'error': 'Retrieval failed',
            'message': str(e)
        }), 500


@app.route('/storage/<path:username>/<path:folder>/<path:filename>')
@require_login
def serve_file(username, folder, filename):
    """
    Serve user's uploaded files (with Minio support)
    """
    try:
        # Check if user is accessing their own files
        if session['username'] != username:
            print(f"Unauthorized access attempt: {session['username']} trying to access {username}'s files")
            return jsonify({
                'error': 'Unauthorized',
                'message': 'You can only access your own files'
            }), 403
        
        print(f"Serving file: {username}/{folder}/{filename}")
        
        # Try to get from Minio first
        if MINIO_ENABLED:
            minio_path = f"{username}/{folder}/{filename}"
            print(f"Attempting to download from Minio: {minio_path}")
            file_data = download_from_minio(minio_path)
            
            if file_data:
                print(f"File retrieved from Minio, size: {len(file_data)} bytes")
                # Determine content type
                mime_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
                print(f"Serving with mime type: {mime_type}")
                return send_file(
                    BytesIO(file_data),
                    mimetype=mime_type,
                    as_attachment=False,
                    download_name=filename
                )
            else:
                print(f"File not found in Minio, trying local storage")
        
        # Fallback to local storage
        folder_path = os.path.join(STORAGE_BASE, username, folder)
        file_path = os.path.join(folder_path, filename)
        print(f"Trying local storage: {file_path}")
        
        if os.path.exists(file_path):
            print(f"Serving from local storage")
            return send_from_directory(folder_path, filename)
        else:
            print(f"File not found in local storage")
            raise FileNotFoundError()
            
    except FileNotFoundError:
        print(f"File not found: {username}/{folder}/{filename}")
        return jsonify({
            'error': 'File not found',
            'message': f'The requested file does not exist'
        }), 404
    except Exception as e:
        print(f"Error serving file: {str(e)}")
        return jsonify({
            'error': 'Server error',
            'message': str(e)
        }), 500


@app.route('/storage-raw/<path:username>/<path:folder>/<path:filename>')
@require_login
def serve_file_raw(username, folder, filename):
    """
    Serve raw file without HTML wrapper
    """
    try:
        # Check if user is accessing their own files
        if session['username'] != username:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'You can only access your own files'
            }), 403
        
        # Try Minio first
        if MINIO_ENABLED:
            minio_path = f"{username}/{folder}/{filename}"
            file_data = download_from_minio(minio_path)
            
            if file_data:
                mime_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
                return send_file(
                    BytesIO(file_data),
                    mimetype=mime_type,
                    as_attachment=False,
                    download_name=filename
                )
        
        # Fallback to local
        folder_path = os.path.join(STORAGE_BASE, username, folder)
        return send_from_directory(folder_path, filename)
    
    except FileNotFoundError:
        return jsonify({
            'error': 'File not found',
            'message': f'The requested file does not exist'
        }), 404


@app.route('/download/<path:username>/<path:folder>/<path:filename>')
@require_login
def download_file(username, folder, filename):
    """
    Download user's uploaded files (forces download instead of preview)
    """
    try:
        # Check if user is accessing their own files
        if session['username'] != username:
            print(f"Unauthorized download attempt: {session['username']} trying to download {username}'s files")
            return jsonify({
                'error': 'Unauthorized',
                'message': 'You can only access your own files'
            }), 403
        
        print(f"Downloading file: {username}/{folder}/{filename}")
        
        # Try to get from Minio first
        if MINIO_ENABLED:
            minio_path = f"{username}/{folder}/{filename}"
            print(f"Attempting to download from Minio: {minio_path}")
            file_data = download_from_minio(minio_path)
            
            if file_data:
                print(f"File retrieved from Minio for download, size: {len(file_data)} bytes")
                # Determine content type
                mime_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
                return send_file(
                    BytesIO(file_data),
                    mimetype=mime_type,
                    as_attachment=True,  # Force download
                    download_name=filename
                )
            else:
                print(f"File not found in Minio for download, trying local storage")
        
        # Fallback to local storage
        folder_path = os.path.join(STORAGE_BASE, username, folder)
        file_path = os.path.join(folder_path, filename)
        print(f"Trying local storage for download: {file_path}")
        
        if os.path.exists(file_path):
            print(f"Downloading from local storage")
            return send_from_directory(folder_path, filename, as_attachment=True)
        else:
            print(f"File not found in local storage for download")
            raise FileNotFoundError()
            
    except FileNotFoundError:
        print(f"Download failed - file not found: {username}/{folder}/{filename}")
        return jsonify({
            'error': 'File not found',
            'message': f'The requested file does not exist'
        }), 404
    except Exception as e:
        print(f"Download error: {str(e)}")
        import traceback
        traceback.print_exc()
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
            'total_json': len(uploads.get('json_data', [])),
            'storage_type': 'Minio Cloud' if MINIO_ENABLED else 'Local',
            'recent_uploads': []
        }
        
        # Get recent uploads (last 5)
        all_uploads = []
        for img in uploads.get('images', []):
            all_uploads.append({**img, 'type': 'image'})
        for vid in uploads.get('videos', []):
            all_uploads.append({**vid, 'type': 'video'})
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


@app.route('/json-database', methods=['GET'])
@require_login
def get_json_database():
    """
    Get all JSON database entries for the logged-in user
    """
    try:
        username = session['username']
        entries = db_manager.get_user_json_entries(username)
        
        return jsonify({
            'success': True,
            'entries': entries,
            'count': len(entries)
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': 'Failed to load database',
            'message': str(e)
        }), 500


@app.route('/json-database/<int:entry_id>', methods=['GET'])
@require_login
def get_json_entry(entry_id):
    """
    Get a specific JSON database entry by ID with flattened data for SQL type
    """
    try:
        username = session['username']
        entry = db_manager.get_entry_by_id(entry_id, username)
        
        if not entry:
            return jsonify({
                'error': 'Not found',
                'message': 'Entry not found or access denied'
            }), 404
        
        # If SQL type, include flattened data
        if entry['storage_type'] == 'sql':
            entry['flattened_data'] = db_manager.get_flattened_data(entry_id)
        
        return jsonify({
            'success': True,
            'entry': entry
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': 'Failed to load entry',
            'message': str(e)
        }), 500


@app.route('/json-database/<int:entry_id>', methods=['DELETE'])
@require_login
def delete_json_entry(entry_id):
    """
    Delete a specific JSON database entry by ID
    """
    try:
        username = session['username']
        
        # Verify the entry exists and belongs to the user
        entry = db_manager.get_entry_by_id(entry_id, username)
        if not entry:
            return jsonify({
                'error': 'Not found',
                'message': 'Entry not found or access denied'
            }), 404
        
        # Delete from Minio if enabled
        if MINIO_ENABLED:
            minio_path = f"{username}/json_data/{entry['filename']}"
            delete_from_minio(minio_path)
        
        # Delete the entry
        success = db_manager.delete_entry(entry_id, username)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Entry deleted successfully'
            }), 200
        else:
            return jsonify({
                'error': 'Delete failed',
                'message': 'Failed to delete entry'
            }), 500
    
    except Exception as e:
        return jsonify({
            'error': 'Failed to delete entry',
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
        'version': '3.0 with Minio Cloud Storage',
        'status': 'running',
        'storage': 'Minio Cloud' if MINIO_ENABLED else 'Local',
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
        'timestamp': datetime.now().isoformat(),
        'storage': 'minio' if MINIO_ENABLED else 'local'
    }), 200


if __name__ == '__main__':
    print("=" * 50)
    print("Intelligent Multi-Modal Storage System v3.0")
    print("With Minio Cloud Storage Integration")
    print("=" * 50)
    create_storage_folders()
    print("\n✓ Server initialization complete!")
    print("✓ Authentication enabled")
    print(f"✓ Storage: {'Minio Cloud' if MINIO_ENABLED else 'Local Filesystem'}")
    print("✓ Listening on: http://127.0.0.1:5000")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)