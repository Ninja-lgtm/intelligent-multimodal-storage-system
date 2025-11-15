# 🎯 Intelligent Multi-Modal Storage System

A college project that automatically classifies and stores different types of data:
- **Images** → `storage/images/`
- **Videos** → `storage/videos/`
- **JSON Data** → `storage/json_data/` (with SQL/NoSQL classification)

---

## 📁 Project Structure

```
Multi-Modal Storage/
├── backend/
│   ├── app.py              # Flask backend server
│   ├── requirements.txt    # Python dependencies
│   └── storage/            # Auto-created storage folders
│       ├── images/
│       ├── videos/
│       └── json_data/
├── frontend/
│   ├── index.html          # Web interface
│   └── style.css           # Styling
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
2. Right-click on `index.html`
3. Open with your browser (Chrome/Edge recommended)

**OR** use the command:

```powershell
start frontend\index.html
```

---

## 🎨 How to Use

1. **Upload an Image or Video:**
   - Click "Choose a file..." button
   - Select an image (JPG, PNG, GIF) or video (MP4, AVI, MOV)
   - Click "Upload & Classify"

2. **Submit JSON Data:**
   - Paste JSON in the textarea
   - System auto-detects SQL vs NoSQL
   - Click "Upload & Classify"

3. **Add Comments (Optional):**
   - Add metadata or description in the comment field

---

## 🔍 Features

✅ **Automatic File Type Detection** - Uses MIME types  
✅ **Smart JSON Classification** - SQL vs NoSQL analysis  
✅ **Timestamped Filenames** - Prevents conflicts  
✅ **Beautiful UI** - Modern, responsive design  
✅ **Real-time Feedback** - Success/error messages  
✅ **CORS Enabled** - Frontend-backend communication  

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
| `/upload` | POST | Upload files or JSON data |
| `/health` | GET | Health check |

---

## 🛠️ Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **CORS**: flask-cors
- **File Handling**: Werkzeug

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
**Solution**: Make sure `style.css` is in the same `frontend` folder as `index.html`

---

## 📌 Important Notes

1. Keep the backend server running while using the frontend
2. Storage folders are created automatically on first run
3. Files are saved with timestamps to prevent overwriting
4. Supported image formats: PNG, JPG, JPEG, GIF, BMP, WEBP, SVG
5. Supported video formats: MP4, AVI, MOV, MKV, FLV, WMV, WEBM

---

## 🎓 College Project Information

This project demonstrates:
- Full-stack web development
- RESTful API design
- File upload handling
- Data classification algorithms
- Modern UI/UX design
- Client-server architecture

---

**Happy Coding! 🚀**
