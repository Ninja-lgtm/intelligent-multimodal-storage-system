"""
Minio Configuration File
Separate your credentials from the main application

Usage:
1. Copy this file and rename to 'config_local.py'
2. Update with your actual credentials
3. Add 'config_local.py' to .gitignore
4. Import in app.py: from config_local import *
"""

# ==================== MINIO CONFIGURATION ====================

# Option 1: Public Minio Demo (Testing Only - Not for production)
# MINIO_ENDPOINT = "play.min.io"
# MINIO_ACCESS_KEY = "minioadmin"
# MINIO_SECRET_KEY = "minioadmin"
# MINIO_BUCKET = "intelligent-storage-demo"
# MINIO_SECURE = True

# Option 2: Minio.io Cloud Service (Recommended for Production)
MINIO_ENDPOINT = "your-account.minio.io"  # Replace with your Minio endpoint
MINIO_ACCESS_KEY = "your-access-key-here"  # Replace with your access key
MINIO_SECRET_KEY = "your-secret-key-here"  # Replace with your secret key
MINIO_BUCKET = "intelligent-storage"       # Your bucket name
MINIO_SECURE = True                        # Use HTTPS

# Option 3: Self-Hosted Local Minio
# MINIO_ENDPOINT = "localhost:9000"
# MINIO_ACCESS_KEY = "minioadmin"
# MINIO_SECRET_KEY = "minioadmin"
# MINIO_BUCKET = "intelligent-storage"
# MINIO_SECURE = False  # No HTTPS for local

# ==================== APPLICATION CONFIGURATION ====================

# Flask Secret Key (Change this to a random string in production)
SECRET_KEY = "change-this-to-a-random-secret-key-in-production"

# Storage Configuration
STORAGE_BASE = 'storage'
USERS_DB = 'storage/users.json'

# File Upload Limits (in MB)
MAX_FILE_SIZE_MB = 100

# Allowed Origins for CORS
ALLOWED_ORIGINS = [
    "http://127.0.0.1:5500",
    "http://127.0.0.1:8000",
    "http://localhost:5500",
    "http://localhost:8000",
    "file://",
    "null"
]

# ==================== MINIO BUCKET POLICIES ====================

# Public read policy for viewing files (optional)
PUBLIC_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": "*"},
            "Action": ["s3:GetObject"],
            "Resource": [f"arn:aws:s3:::{MINIO_BUCKET}/*"]
        }
    ]
}

# ==================== GETTING MINIO CREDENTIALS ====================

"""
HOW TO GET MINIO CREDENTIALS:

1. For Minio.io Cloud:
   - Go to https://min.io/
   - Sign up for an account
   - Create a new bucket
   - Generate access keys from console
   - Copy endpoint, access key, and secret key

2. For Self-Hosted Minio:
   Install via Docker:
   
   docker run -p 9000:9000 -p 9001:9001 \
     -e "MINIO_ROOT_USER=minioadmin" \
     -e "MINIO_ROOT_PASSWORD=minioadmin" \
     minio/minio server /data --console-address ":9001"
   
   Then access console at: http://localhost:9001
   Default credentials: minioadmin / minioadmin

3. For AWS S3 (Alternative):
   - You can also use AWS S3 instead of Minio
   - Just change MINIO_ENDPOINT to "s3.amazonaws.com"
   - Use your AWS access key and secret key
   - Set MINIO_SECURE = True
"""

# ==================== ENVIRONMENT VARIABLES (Recommended) ====================

"""
For production, use environment variables instead:

import os

MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'play.min.io')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
MINIO_BUCKET = os.getenv('MINIO_BUCKET', 'intelligent-storage')
MINIO_SECURE = os.getenv('MINIO_SECURE', 'True') == 'True'

Then set environment variables:
export MINIO_ENDPOINT="your-endpoint.minio.io"
export MINIO_ACCESS_KEY="your-access-key"
export MINIO_SECRET_KEY="your-secret-key"
"""