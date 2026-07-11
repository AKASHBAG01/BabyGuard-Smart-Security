# 👶 BabyGuard Smart Security (BGSS)

An AI-powered baby monitoring and surveillance system built with **Python, OpenCV, YOLO, Flask, and Android**. BGSS provides real-time face recognition, object detection, unknown person photo capture, zone monitoring, event logging, live video streaming, and Android remote monitoring to enhance child safety.

---

## 🚀 Features

- 👤 Real-time Face Recognition
- 📦 YOLO-based Object Detection
- 📸 Automatic Unknown Person Photo Capture
- 🎥 Live Camera Streaming
- 📱 Android Monitoring Application
- 📜 Event History
- 🏠 Family Member Management
- 🚪 Zone Monitoring (Bed, Door, Play Area, Wardrobe)
- ⚡ Real-time Status Monitoring
- 🌐 REST API using Flask
- 🔄 Live Dashboard
- 📡 Android-Backend Communication using Retrofit

---

## 🛠️ Technologies Used

### Backend
- Python
- Flask
- OpenCV
- NumPy
- Pickle

### Artificial Intelligence
- YOLOv8
- Haar Cascade Face Detection
- K-Nearest Neighbors (KNN) Face Recognition

### Android
- Java
- Android Studio
- XML
- Retrofit
- WebView

### Communication
- REST API
- HTTP
- JSON

---

## 📂 Project Structure

```
BabyGuard-Smart-Security/
│
├── api/
│   ├── app.py
│   ├── camera.py
│   ├── events.py
│   ├── family.py
│   ├── unknown.py
│   ├── status.py
│   └── add_person.py
│
├── modules/
│   ├── dashboard.py
│   ├── event_logger.py
│   ├── face_recognition.py
│   ├── object_detection.py
│   ├── relationship_detector.py
│   ├── shared_frame.py
│   └── zone_editor.py
│
├── models/
│   ├── yolov8n.pt
│   ├── haarcascade_frontalface_default.xml
│   ├── names.pkl
│   └── faces_data.pkl
│
├── database/
│   ├── family.json
│   └── events.json
│
├── ai_security_system.py
├── add_faces.py
└── README.md
```

---

## 📱 Android Application

The Android application allows users to:

- Watch the live camera feed
- View event history
- Monitor AI detection status
- Receive real-time monitoring information

---

## 🧠 AI Modules

### Face Recognition
Recognizes registered family members using OpenCV and KNN.

### Object Detection
Detects objects in real time using the YOLOv8 model.

### Unknown Person Detection
Captures photos of unknown individuals for security monitoring.

### Zone Monitoring
Monitors important zones including:

- Bed Area
- Door Area
- Play Area
- Wardrobe Area

---

## 🌐 REST API

| Endpoint | Description |
|----------|-------------|
| `/live` | Live Camera Stream |
| `/family` | Family Members |
| `/events` | Event History |
| `/status` | System Status |
| `/unknown` | Unknown Person Images |
| `/add_person` | Register New Family Member |

---


## 🔮 Future Improvements

- Push Notifications
- Cloud Storage
- Firebase Integration
- Multi-Camera Support
- Voice Alerts
- Night Vision Support
- AI Behaviour Analysis
- Fall Detection
- Cry Detection
- Cloud Dashboard

---

## 👨‍💻 Developer

**Akash kumar Bag**

Electronics and Communication Engineering (ECE)

Haldia Institute of Technology

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

---

## 📄 License

This project is intended for educational and research purposes.
