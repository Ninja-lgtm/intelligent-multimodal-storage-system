# 🎯 Intelligent Multi-Modal Storage System

A college project featuring a secure, multi-user storage system that automatically classifies and stores different types of data with user authentication and personal isolated storage:
- **Images** → `storage/{username}/images/`
- **Videos** → `storage/{username}/videos/`
- **PDF Documents** → `storage/{username}/pdfs/`
- **JSON Data** → `storage/{username}/json_data/` (with SQL/NoSQL classification)
- **User Authentication** → Session-based login with password hashing
- **Modal File Viewer** → In-page popup for viewing images, videos, PDFs, and JSON
- **Multiple File Upload** → Upload multiple files at once with batch processing
- **Dual-View JSON Viewer** → Switch between JSON Format and Table Format for better data visualization
- **MinIO Cloud Storage** → Files stored in MinIO cloud server (play.min.io demo)

---

## 📁 Project Structure

```
Multi-Modal Storage/
├── backend/
│   ├── app.py              # Flask backend server
│   ├── requirements.txt    # Python dependencies
├── storage/            # Local storage backup (per-user folders)
│   ├── users.json      # User database with file metadata
│   └── {username}/
│       ├── images/
│       ├── videos/
│       ├── pdfs/
│       └── json_data/
├── frontend/
│   ├── index.html          # Landing page
│   ├── style.css           # Landing page styles
│   ├── login.html          # Login/Registration page
│   ├── login-style.css     # Login page styles
│   ├── dashboard.html      # User dashboard with dual-view JSON viewer
│   ├── dashboard-style.css # Dashboard styles
│   ├── database.html       # JSON Database Explorer
│   └── database-style.css  # Database page styles
└── README.md              # This file
```

---

## 🚀 Setup Instructions

### Step 1: Install Python Dependencies

Open PowerShell in the `backend` folder and run:

```powershell
cd backend
pip install -r requirements.txt
```

**Dependencies installed:**
- Flask 3.0.0 (Web framework)
- flask-cors 4.0.0 (Cross-origin support)
- Werkzeug 3.0.1 (Security utilities)
- minio 7.2.18 (Cloud storage client)

### Step 2: Run the Backend Server

```powershell
python app.py
```

You should see:
```
==================================================
Intelligent Multi-Modal Storage System
==================================================
✓ Created folder: storage\images
✓ Created folder: storage\videos
✓ Created folder: storage\json_data

✓ Server initialization complete!
✓ Endpoint: POST /upload
✓ Listening on: http://127.0.0.1:5000
==================================================
```

### Step 3: Open the Frontend

1. Navigate to the `frontend` folder
2. Open `index.html` in your browser (Chrome/Edge recommended)
3. Click "Get Started" to go to login page
4. Register a new account or login with existing credentials

**OR** use the command:

```powershell
start frontend\index.html
```

**Quick Start URLs:**
- Landing Page: `frontend/index.html`
- Login/Register: `frontend/login.html`
- Dashboard: `frontend/dashboard.html` (requires login)

---

## 🎨 How to Use

### 1. **Register/Login:**
   - Create a new account with username and password
   - Or login with existing credentials
   - Passwords are securely hashed using Werkzeug

### 2. **Upload Files:**
   - **Unified Upload**: Single file input accepts all file types
   - **Multiple Files**: Hold Ctrl (Windows) or Cmd (Mac) to select multiple files
   - **Supported Formats**:
     - Images: JPG, PNG, GIF, BMP, WEBP, SVG
     - Videos: MP4, AVI, MOV, MKV, FLV, WMV, WEBM
     - Documents: PDF
     - Data: JSON (upload file or paste in textarea)
   - Add optional comments/metadata
   - Click "Upload & Classify"
   - System auto-detects file type and stores in correct folder

### 3. **View Your Files:**
   - Click "🗂️ Retrieve Data" to see all your files
   - Files are organized by category (Images, Videos, PDFs, JSON)
   - **Enhanced Modal Popup Viewer**:
     - Click "👁️ View File" to open in-page popup modal
     - View images, videos, and PDFs without leaving the page
     - **Dual-View JSON Viewer** with tab switching:
       - **📄 JSON Format**: Syntax-highlighted JSON with dark theme
       - **📊 Table Format**: Beautiful tabular representation
         - **SQL Data** (flat objects): 2-column Field/Value table
         - **NoSQL Data** (arrays): Multi-column database-style table
     - Color-coded data types (NULL, Boolean, Number, String, Array, Object)
     - PDFs displayed in embedded viewer
     - Optimized modal sizing (95vh height, 1200px max-width)
     - Close with X button, Escape key, or click outside
   - Click "⬇️ Download" to save files locally
   - **Cloud Storage**: Files automatically uploaded to MinIO cloud server

### 4. **Logout:**
   - Click the logout button to end your session securely

---

## 🔍 Features

### Core Features
✅ **User Authentication** - Secure login/registration with password hashing  
✅ **Personal Storage** - Isolated storage per user  
✅ **Unified Upload System** - Single input for all file types (images, videos, PDFs, JSON)  
✅ **Multiple File Upload** - Upload multiple files at once with batch processing  
✅ **Automatic File Type Detection** - Uses MIME types for auto-classification  
✅ **Smart JSON Classification** - SQL vs NoSQL analysis  
✅ **PDF Support** - Upload and view PDF documents in-browser  
✅ **Timestamped Filenames** - Prevents conflicts  
✅ **Session Management** - Secure server-side sessions  

### UI/UX Features
✅ **Enhanced Modal Popup Viewer** - Optimized sizing (95vh, 1200px) with overflow handling  
✅ **Dual-View JSON Viewer** - Switch between JSON Format and Table Format with tabs  
✅ **Smart Table Generation**:  
   - SQL data → 2-column Field/Value table with row numbers  
   - NoSQL data → Multi-column database-style table with headers  
✅ **Color-Coded Data Types** - Visual differentiation (NULL, Boolean, Number, String, Array, Object)  
✅ **Purple Gradient Tabs** - High-visibility active state with smooth transitions  
✅ **PDF Viewer** - Embedded PDF viewer in modal popup (75vh height for comfortable reading)  
✅ **PDF Visual Enhancements** - Red accent colors, special hover effects, left border indicators  
✅ **Batch Upload Results** - Visual summary of multi-file uploads  
✅ **Progress Tracking** - Real-time upload progress for multiple files  
✅ **2x2 Feature Grid** - Clean landing page layout  
✅ **Responsive Design** - Works on desktop and mobile  
✅ **Modern UI** - Gradient backgrounds, glassmorphism effects  
✅ **Real-time Feedback** - Success/error messages with file-by-file status  
✅ **Keyboard Shortcuts** - ESC to close modal  
✅ **JSON Database Explorer** - Separate page to browse all JSON files with filtering  

### Technical Features
✅ **MinIO Cloud Storage** - Files stored in MinIO cloud server (play.min.io demo)  
✅ **Hybrid Storage** - Cloud-first with local backup fallback  
✅ **PDF Upload & Storage** - Full PDF support with dedicated folder structure  
✅ **File Metadata Tracking** - users.json database with minio_path field  
✅ **CORS Enabled** - Frontend-backend communication  
✅ **Dual Download Endpoints** - /storage (preview) and /download (download)  
✅ **Secure File Serving** - Uses absolute paths with send_file  
✅ **Body Scroll Lock** - No background scrolling when modal open  
✅ **Sequential Upload** - Multiple files uploaded one by one with error handling  
✅ **Mixed Result Handling** - Displays both successful and failed uploads  
✅ **Extensive Logging** - Console debugging for file operations  

---

## 📊 JSON Classification Logic

- **SQL Database**: Simple key-value pairs only
  ```json
  {"name": "John", "age": 25, "city": "Mumbai"}
  ```

- **NoSQL Database**: Nested objects or arrays
  ```json
  {"name": "John", "skills": ["Python", "AI"], "address": {"city": "Mumbai"}}
  ```

---

## ⚙️ API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Server status check |
| `/register` | POST | Register new user account |
| `/login` | POST | User login (creates session) |
| `/logout` | POST | User logout (destroys session) |
| `/upload` | POST | Upload file(s) or JSON data (authenticated, supports multiple files) |
| `/retrieve` | GET | Get user's files list including PDFs (authenticated) |
| `/storage/<user>/<folder>/<file>` | GET | View/preview file in browser (cloud-first with local fallback) |
| `/download/<user>/<folder>/<file>` | GET | Download file with proper attachment headers |
| `/dashboard-stats` | GET | Get user statistics (file counts) |
| `/json-database` | GET | Get all JSON files for database explorer (authenticated) |
| `/json-database/<id>` | GET | Get specific JSON entry details |
| `/health` | GET | Health check |

---

## 🛠️ Technologies Used

### Backend
- **Framework**: Flask 3.0.0 (Python)
- **CORS**: flask-cors 4.0.0
- **Security**: Werkzeug 3.0.1 (password hashing)
- **Sessions**: Flask server-side sessions
- **Cloud Storage**: MinIO 7.2.18 (play.min.io demo server)
- **File Handling**: send_file with MIME type detection
- **Database**: users.json (JSON-based file metadata storage)

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Gradients, animations, flexbox, grid
- **JavaScript**: Vanilla JS (no frameworks)
- **UI Effects**: Glassmorphism, modal overlays, backdrop blur

### Architecture
- **Client-Server**: RESTful API communication
- **Session-Based Auth**: Server-side session management
- **Per-User Storage**: Isolated file systems

---

## 📝 Author

**Triple Threat**  
College Project • November 2025

---

## 🐛 Troubleshooting

### Issue: "Connection Error"
**Solution**: Ensure the backend server is running on `http://127.0.0.1:5000`

### Issue: "Import 'flask_cors' could not be resolved"
**Solution**: Run `pip install -r requirements.txt` in the backend folder

### Issue: "No module named 'flask'"
**Solution**: Install Flask: `pip install flask flask-cors`

### Issue: CSS not loading
**Solution**: Ensure CSS files are in the `frontend` folder with correct filenames

### Issue: "Please log in" error
**Solution**: Login through `login.html` first to create a session

### Issue: Modal not closing
**Solution**: Click the X button, press ESC key, or click outside the modal

### Issue: Files not downloading
**Solution**: Check browser download settings and popup blockers

### Issue: Can't view uploaded files
**Solution**: Ensure you're logged in as the same user who uploaded the files

### Issue: Multiple file upload not working
**Solution**: Hold Ctrl (Windows) or Cmd (Mac) when selecting files, ensure all files are supported formats

### Issue: PDF not displaying in modal
**Solution**: Ensure browser allows embedded PDFs, try downloading if viewer doesn't load. Some browsers block PDF iframes - use Chrome/Edge for best experience

### Issue: PDF upload not working
**Solution**: Restart backend server to load new PDF handling code, ensure file extension is .pdf, check that file size is reasonable

### Issue: Table view not showing for JSON
**Solution**: Hard refresh browser (Ctrl+Shift+R), clear cache, check console for errors

### Issue: Modal content overflowing/not fitting
**Solution**: New modal sizing applied (95vh, 1200px), hard refresh to load updated CSS

### Issue: Can't preview old uploaded files
**Solution**: Old files stored locally, new files in MinIO cloud - backend has fallback logic

### Issue: MinIO connection errors
**Solution**: Using public demo server (play.min.io), check internet connection

---

## 📌 Important Notes

1. Keep the backend server running while using the frontend
2. **User Authentication Required**: Register/login before uploading files
3. **Per-User Storage**: Each user has isolated storage folders
4. **Multiple File Upload**: Select multiple files at once (Ctrl+Click or Cmd+Click)
5. Storage folders are created automatically per user
6. Files are saved with timestamps to prevent overwriting
7. **Session-Based**: Sessions persist until logout or server restart
8. Passwords are hashed using Werkzeug (never stored as plain text)
9. **Supported Formats**:
   - Images: PNG, JPG, JPEG, GIF, BMP, WEBP, SVG
   - Videos: MP4, AVI, MOV, MKV, FLV, WMV, WEBM
   - Documents: PDF (uploaded to dedicated pdfs/ folder)
   - Data: JSON
10. **Modal Viewer**: View files in-page without opening new tabs (PDFs in 75vh iframe)
11. **Batch Processing**: Upload multiple files with individual success/error tracking
12. **Dual-View JSON Viewer**: Switch between JSON Format (📄) and Table Format (📊)
13. **MinIO Cloud Storage**: Files automatically uploaded to cloud (bucket: intelligent-storage)
14. **Hybrid Storage**: New files in cloud, old files local, seamless fallback
15. **Enhanced Modal Sizing**: 95vh height, 1200px width, optimized for tables
16. **JSON Database Explorer**: Browse all JSON files at `/json-database` endpoint

---

## 🎓 College Project Information

This project demonstrates:
- Full-stack web development (Flask + Vanilla JS)
- RESTful API design
- User authentication & authorization
- Session management
- Password hashing & security
- **Multiple file upload handling** with batch processing
- **PDF document management** and in-browser viewing
- File upload/download handling with MIME type detection
- Per-user data isolation
- Data classification algorithms (SQL vs NoSQL)
- Modern UI/UX design (glassmorphism, gradients, animations)
- Modal popup implementation with embedded viewers
- Client-server architecture
- Responsive web design (2x2 grid, flexbox, CSS grid)
- **Error handling** for individual files in batch uploads
- **Progress tracking** for multiple simultaneous operations
- **Advanced JSON visualization** with dual-view (JSON/Table format)
- **Cloud storage integration** (MinIO object storage)
- **Hybrid storage architecture** (cloud-first with local fallback)
- **Dynamic table generation** from JSON data (SQL vs NoSQL)
- **Type-aware rendering** (color-coded data types)
- **Metadata tracking** with users.json database

---

**Happy Coding! 🚀**
