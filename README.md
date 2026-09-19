# 👶 BabyGuard Smart Security (BGSS)

An AI-powered baby monitoring and surveillance system built with **Python, OpenCV, YOLO, Flask, and Android**.

BabyGuard Smart Security (BGSS) provides real-time face recognition, object detection, unknown person photo capture, zone monitoring, event logging, live video streaming, and Android-based remote monitoring to enhance child safety.

---

## 🚀 Features

- 👤 Real-time Face Recognition
- 📦 YOLO-based Object Detection
- 📸 Automatic Unknown Person Photo Capture
- 🎥 Live Camera Streaming
- 📱 Android Monitoring Application
- 📜 Event History
- 👥 Registered Family Member Monitoring
- 🚪 Zone Monitoring
- ⚡ Real-time Status Monitoring
- 🌐 REST API using Flask
- 🔄 Live Security Dashboard
- 📡 Android-Backend Communication using Retrofit
- 🖥️ Python-based AI Security Processing

---

## 🏗️ Project Architecture

BabyGuard Smart Security consists of two separate repositories that work together as one project.

### 🐍 1. Python Backend & AI System

**Repository:**  
`BabyGuard-Smart-Security`

This repository contains:

- AI processing
- Face recognition
- Object detection
- Camera processing
- Zone monitoring
- Event logging
- Unknown person detection
- Flask REST API
- Live security dashboard

### 📱 2. Android Application

**Repository:**  
`BabyGuard-Android`

The Android application provides a mobile interface for monitoring the Python backend.

**Android Repository:**  
https://github.com/AKASHBAG01/BabyGuard-Android

---

## 🔄 System Architecture

```text
                  ┌─────────────────────┐
                  │   Camera / Webcam   │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   Python AI System  │
                  │                     │
                  │ OpenCV              │
                  │ Face Recognition    │
                  │ YOLOv8              │
                  │ Zone Monitoring     │
                  │ Event Detection     │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   Flask Backend     │
                  │      REST API       │
                  └──────────┬──────────┘
                             │
                      HTTP / REST / JSON
                             │
                             ▼
                  ┌─────────────────────┐
                  │    Android App      │
                  │                     │
                  │ Live Camera         │
                  │ Event History       │
                  │ Family Members      │
                  │ System Monitoring   │
                  └─────────────────────┘
````

---

## 🛠️ Technologies Used

### Backend

* Python
* Flask
* OpenCV
* NumPy
* Pickle

### Artificial Intelligence & Computer Vision

* YOLOv8
* Haar Cascade Face Detection
* K-Nearest Neighbors (KNN) Face Recognition
* Computer Vision

### Android

* Java
* Android Studio
* XML
* Retrofit
* WebView

### Communication

* REST API
* HTTP
* JSON

---

## 📂 Project Structure

```text
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
│   └── haarcascade_frontalface_default.xml
│
├── database/
│   ├── family.json
│   └── events.json
│
├── ai_security_system.py
├── add_faces.py
├── requirements.txt
└── README.md
```

> **Note:** `names.pkl` and `faces_data.pkl` are generated locally during face registration and are not included in the GitHub repository.

---

# 🧠 AI Modules

## 👤 Face Recognition

The system uses **Haar Cascade** for face detection and **K-Nearest Neighbors (KNN)** for recognizing registered family members.

The face registration system collects face samples and generates the required recognition data locally.

---

## 📦 Object Detection

The system uses the **YOLOv8** deep learning model for real-time object detection.

The camera frames are continuously processed to identify supported objects in the environment.

---

## 📸 Unknown Person Detection

When an unknown person is detected, the system can automatically capture and save an image for security monitoring.

This allows the user to review unknown-person events later.

---

## 🚪 Zone Monitoring

The system supports monitoring different areas of the environment.

Example zones include:

* 🛏️ Bed Area
* 🚪 Door Area
* 🧸 Play Area
* 🗄️ Wardrobe Area

Zones can be configured according to the camera view.

---

## 📜 Event Logging

Security-related events are recorded with timestamps.

Recent events are stored by the backend and can be retrieved by the Android application through the REST API.

---

# 🌐 REST API

The Flask backend provides REST API endpoints for communication with the Android application.

| Endpoint      | Description                |
| ------------- | -------------------------- |
| `/`           | Backend Home / Status      |
| `/live`       | Live Camera Stream         |
| `/family`     | Registered Family Members  |
| `/events`     | Security Event History     |
| `/status`     | System Status              |
| `/unknown`    | Unknown Person Information |
| `/add_person` | Register New Family Member |

---

# 📱 Android Application

The Android application is maintained in a separate repository.

### Android Repository

**BabyGuard-Android**

[https://github.com/AKASHBAG01/BabyGuard-Android](https://github.com/AKASHBAG01/BabyGuard-Android)

The Android application provides a mobile interface for monitoring the BabyGuard backend.

### Android Features

* 🎥 Live camera monitoring
* 📜 Event history
* 👥 View registered family members
* 📊 Monitor security status
* 📡 Communicate with the Flask backend
* 🌐 Display live backend dashboard

> **Note:** Family member registration is currently handled through the Python/backend system. The Android application is primarily used for monitoring.

---

# 🔄 Android ↔ Backend Communication

The Android application communicates with the Python Flask backend over the local network.

```text
Android Phone
      │
      │ HTTP / REST API
      ▼
Flask Backend
      │
      ▼
Python AI Security System
      │
      ▼
Camera + AI Processing
```

### Retrofit

**Retrofit** is used in the Android application to communicate with Flask REST API endpoints such as:

```text
GET /family
GET /events
```

### WebView

The Android application uses **WebView** to display the live camera/dashboard provided by:

```text
/live
```

---

# ⚙️ Installation

## 1. Clone the Backend Repository

```bash
git clone https://github.com/AKASHBAG01/BabyGuard-Smart-Security.git
```

Move into the project directory:

```bash
cd BabyGuard-Smart-Security
```

---

## 2. Create a Virtual Environment

On Windows:

```bash
python -m venv venv
```

Activate the environment:

```powershell
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the Backend

```bash
python ai_security_system.py
```

The Flask backend will run on:

```text
http://127.0.0.1:5000
```

---

# 📱 Android Setup

Clone the Android repository:

```bash
git clone https://github.com/AKASHBAG01/BabyGuard-Android.git
```

Open the project in **Android Studio**.

Before running the application, update the backend IP address in:

```text
ApiClient.java
```

Example:

```java
private static final String BASE_URL =
        "http://YOUR_COMPUTER_IP:5000/";
```

Also update the live camera URL in:

```text
LiveCameraActivity.java
```

Example:

```java
webView.loadUrl(
        "http://YOUR_COMPUTER_IP:5000/live"
);
```

---

# 🌐 Network Requirement

The Android phone and the computer running the Python backend must be connected to the **same local network**.

Example:

```text
Computer
192.168.1.7
     │
     │ Same Wi-Fi
     │
Android Phone
192.168.1.x
```

The Android application communicates with:

```text
http://YOUR_COMPUTER_IP:5000/
```

> **Note:** The computer's IP address may change depending on the local network. Update the Android application if the IP address changes.

---

# 🔮 Future Improvements

* 🔔 Push Notifications
* ☁️ Cloud Storage
* 🔥 Firebase Integration
* 📹 Multi-Camera Support
* 🔊 Voice Alerts
* 🌙 Night Vision Support
* 🧠 Advanced AI Behaviour Analysis
* 🚨 Fall Detection
* 👶 Baby Cry Detection
* ☁️ Cloud-Based Monitoring Dashboard
* 🌐 Internet-Based Remote Monitoring
* 📱 Improved Android Controls

---

# 👨‍💻 Developer

**Akash kumar Bag**

Electronics and Communication Engineering (ECE)

Haldia Institute of Technology

---

# 🔗 Related Repository

### 📱 Android Application

**BabyGuard-Android**

[https://github.com/AKASHBAG01/BabyGuard-Android](https://github.com/AKASHBAG01/BabyGuard-Android)

This repository contains the Android application that connects to the BabyGuard Smart Security Python backend.

---

# ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

# 📄 License

This project is intended for educational and research purposes.

```
```
