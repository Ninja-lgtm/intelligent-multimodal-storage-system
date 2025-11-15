# 🎯 Intelligent Multi-Modal Storage System

A college project featuring a secure, multi-user storage system that automatically classifies and stores different types of data with user authentication and personal isolated storage:
- **Images** → `storage/{username}/images/`
- **Videos** → `storage/{username}/videos/`
- **PDF Documents** → `storage/{username}/pdfs/`
- **JSON Data** → `storage/{username}/json_data/` (with SQL/NoSQL classification)
- **User Authentication** → Session-based login with password hashing
- **Modal File Viewer** → In-page popup for viewing images, videos, PDFs, and JSON
- **Multiple File Upload** → Upload multiple files at once with batch processing

---

## 📁 Project Structure

```
Multi-Modal Storage/
├── backend/
│   ├── app.py              # Flask backend server
│   ├── requirements.txt    # Python dependencies
├── storage/            # Per-user storage folders
│       └── {username}/
│           ├── images/
│           ├── videos/
│           ├── pdfs/
│           └── json_data/
├── frontend/
│   ├── index.html          # Landing page
│   ├── style.css           # Landing page styles
│   ├── login.html          # Login/Registration page
│   ├── login-style.css     # Login page styles
│   ├── dashboard.html      # User dashboard
│   └── dashboard-style.css # Dashboard styles
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
   - **Modal Popup Viewer**:
     - Click "👁️ View File" to open in-page popup modal
     - View images, videos, and PDFs without leaving the page
     - See formatted JSON with syntax highlighting
     - PDFs displayed in embedded viewer
     - Close with X button, Escape key, or click outside
   - Click "⬇️ Download" to save files locally

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
✅ **Modal Popup Viewer** - In-page file viewing with smooth animations  
✅ **PDF Viewer** - Embedded PDF viewer in modal popup  
✅ **Batch Upload Results** - Visual summary of multi-file uploads  
✅ **Progress Tracking** - Real-time upload progress for multiple files  
✅ **2x2 Feature Grid** - Clean landing page layout  
✅ **Responsive Design** - Works on desktop and mobile  
✅ **Modern UI** - Gradient backgrounds, glassmorphism effects  
✅ **Real-time Feedback** - Success/error messages with file-by-file status  
✅ **Keyboard Shortcuts** - ESC to close modal  

### Technical Features
✅ **CORS Enabled** - Frontend-backend communication  
✅ **File Download** - Dedicated download endpoint  
✅ **Secure File Serving** - Uses absolute paths with send_file  
✅ **Body Scroll Lock** - No background scrolling when modal open  
✅ **Sequential Upload** - Multiple files uploaded one by one with error handling  
✅ **Mixed Result Handling** - Displays both successful and failed uploads  

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
| `/storage/<user>/<folder>/<file>` | GET | View file in browser (images, videos, PDFs, JSON) |
| `/download/<user>/<folder>/<file>` | GET | Download file |
| `/dashboard-stats` | GET | Get user statistics (file counts) |
| `/health` | GET | Health check |

---

## 🛠️ Technologies Used

### Backend
- **Framework**: Flask 3.0.0 (Python)
- **CORS**: flask-cors 4.0.0
- **Security**: Werkzeug 3.0.1 (password hashing)
- **Sessions**: Flask server-side sessions
- **File Handling**: send_file with MIME type detection

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

**Kumar Amityush**  
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
**Solution**: Ensure browser allows embedded PDFs, try downloading if viewer doesn't load

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
   - Documents: PDF
   - Data: JSON
10. **Modal Viewer**: View files in-page without opening new tabs
11. **Batch Processing**: Upload multiple files with individual success/error tracking

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

---

**Happy Coding! 🚀**
