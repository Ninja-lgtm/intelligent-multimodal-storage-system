# 🎯 Intelligent Multi-Modal Storage System

A college project featuring a secure, multi-user storage system that automatically classifies and stores different types of data with user authentication and personal isolated storage:
- **Images** → `storage/{username}/images/`
- **Videos** → `storage/{username}/videos/`
- **JSON Data** → `storage/{username}/json_data/` (with SQL/NoSQL classification)
- **User Authentication** → Session-based login with password hashing
- **Modal File Viewer** → In-page popup for viewing images, videos, and JSON

---

## 📁 Project Structure

```
Multi-Modal Storage/
├── backend/
│   ├── app.py              # Flask backend server
│   ├── requirements.txt    # Python dependencies
|── storage/            # Per-user storage folders
│       └── {username}/
│           ├── images/
│           ├── videos/
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
   - **Images**: Click "Choose a file..." and select JPG, PNG, GIF, etc.
   - **Videos**: Click "Choose a file..." and select MP4, AVI, MOV, etc.
   - **JSON Data**: Paste JSON in the textarea (auto-classified as SQL/NoSQL)
   - Add optional comments/metadata
   - Click "Upload & Classify"

### 3. **View Your Files:**
   - Click "🗂️ Retrieve Data" to see all your files
   - Files are organized by category (Images, Videos, JSON)
   - **Modal Popup Viewer**:
     - Click "👁️ View File" to open in-page popup modal
     - View images and videos without leaving the page
     - See formatted JSON with syntax highlighting
     - Close with X button, Escape key, or click outside
   - Click "⬇️ Download" to save files locally

### 4. **Logout:**
   - Click the logout button to end your session securely

---

## 🔍 Features

### Core Features
✅ **User Authentication** - Secure login/registration with password hashing  
✅ **Personal Storage** - Isolated storage per user  
✅ **Automatic File Type Detection** - Uses MIME types  
✅ **Smart JSON Classification** - SQL vs NoSQL analysis  
✅ **Timestamped Filenames** - Prevents conflicts  
✅ **Session Management** - Secure server-side sessions  

### UI/UX Features
✅ **Modal Popup Viewer** - In-page file viewing with smooth animations  
✅ **2x2 Feature Grid** - Clean landing page layout  
✅ **Responsive Design** - Works on desktop and mobile  
✅ **Modern UI** - Gradient backgrounds, glassmorphism effects  
✅ **Real-time Feedback** - Success/error messages  
✅ **Keyboard Shortcuts** - ESC to close modal  

### Technical Features
✅ **CORS Enabled** - Frontend-backend communication  
✅ **File Download** - Dedicated download endpoint  
✅ **Secure File Serving** - Uses absolute paths with send_file  
✅ **Body Scroll Lock** - No background scrolling when modal open  

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
| `/upload` | POST | Upload files or JSON data (authenticated) |
| `/retrieve` | POST | Get user's files list (authenticated) |
| `/storage/<user>/<folder>/<file>` | GET | View file in browser |
| `/download/<user>/<folder>/<file>` | GET | Download file |
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

---

## 📌 Important Notes

1. Keep the backend server running while using the frontend
2. **User Authentication Required**: Register/login before uploading files
3. **Per-User Storage**: Each user has isolated storage folders
4. Storage folders are created automatically per user
5. Files are saved with timestamps to prevent overwriting
6. **Session-Based**: Sessions persist until logout or server restart
7. Passwords are hashed using Werkzeug (never stored as plain text)
8. Supported image formats: PNG, JPG, JPEG, GIF, BMP, WEBP, SVG
9. Supported video formats: MP4, AVI, MOV, MKV, FLV, WMV, WEBM
10. **Modal Viewer**: View files in-page without opening new tabs

---

## 🎓 College Project Information

This project demonstrates:
- Full-stack web development (Flask + Vanilla JS)
- RESTful API design
- User authentication & authorization
- Session management
- Password hashing & security
- File upload/download handling
- Per-user data isolation
- Data classification algorithms (SQL vs NoSQL)
- Modern UI/UX design (glassmorphism, gradients, animations)
- Modal popup implementation
- Client-server architecture
- Responsive web design (2x2 grid, flexbox, CSS grid)

---

**Happy Coding! 🚀**
