# 🛡️ DriveSafe AI

> **An AI-powered Driver Drowsiness and Distraction Detection System that monitors driver fatigue in real time using Computer Vision, MediaPipe Face Mesh, OpenCV, and Streamlit.**

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Face%20Mesh-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?logo=sqlite)
![Status](https://img.shields.io/badge/Status-Completed-success)

---

# 🚗 Overview

Driver fatigue and distraction are among the leading causes of road accidents worldwide. **DriveSafe AI** is an intelligent real-time driver monitoring system that leverages **Computer Vision** and **Artificial Intelligence** to detect signs of driver fatigue and distraction.

Using facial landmark analysis, the system continuously monitors the driver's face through a webcam, analyzes eye movements, mouth movements, and head orientation, calculates a dynamic risk score, and immediately alerts the driver whenever unsafe behaviour is detected.

All monitoring data is stored locally in an SQLite database and visualized through an interactive Streamlit dashboard for further analysis.

---

# 🚀 Key Highlights

- Real-time Eye Aspect Ratio (EAR) monitoring
- Intelligent Yawn Detection using Mouth Aspect Ratio (MAR)
- Head Pose Estimation for distraction detection
- Dynamic Driver Risk Score calculation
- Real-time Audio & Visual Alerts
- Smart Break Recommendation System
- SQLite Database Logging
- Interactive Streamlit Dashboard
- Driver Safety Score & Risk Analytics

---

# 🎯 Objectives

The primary objectives of DriveSafe AI are:

- Reduce accidents caused by driver fatigue.
- Detect early signs of drowsiness and distraction.
- Provide real-time warnings to improve road safety.
- Visualize driver behaviour using interactive analytics.
- Demonstrate the practical application of Computer Vision in intelligent transportation systems.

---

# ✨ Features

## 👁️ Eye Monitoring

- Eye Aspect Ratio (EAR) based drowsiness detection
- Continuous eye state monitoring
- Fatigue detection

---

## 😮 Yawn Detection

- Mouth Aspect Ratio (MAR) analysis
- Multi-frame verification
- Reduced false positives

---

## 🎯 Head Pose Estimation

Detects whether the driver is:

- Looking Forward
- Looking Left
- Looking Right

Used for distraction detection.

---

## ⚠️ Dynamic Risk Engine

The Driver Risk Engine calculates a real-time risk score using:

- Eye Closure
- Yawning
- Head Direction

The score gradually increases during unsafe behaviour and decreases once the driver returns to an attentive state.

---

## 🔊 Alert System

- Real-time Audio Alert
- Visual Alert Panel
- Driver Status Indicator
- Break Recommendation

---

## 📊 Analytics Dashboard

Interactive dashboard displaying:

- Driver Safety Score
- Driver Status
- Risk Score
- Risk Timeline
- Eye Aspect Ratio (EAR)
- Mouth Aspect Ratio (MAR)
- Head Pose Distribution
- High Risk Alerts
- Session History

---

# 🖼️ Screenshots
![image alt](https://github.com/paridhiprasanna/DriveSafe-AI/blob/62668e615748e11b422cc7d9f9a90e5a67081ef9/screenshots/DSAI-DASH1.png)
![image alt](https://github.com/paridhiprasanna/DriveSafe-AI/blob/62668e615748e11b422cc7d9f9a90e5a67081ef9/screenshots/DSAI-DASH5.png)
![image alt](https://github.com/paridhiprasanna/DriveSafe-AI/blob/62668e615748e11b422cc7d9f9a90e5a67081ef9/screenshots/DSAI-DASH6.png)


---

# 🏗️ System Architecture

```text
                Webcam
                   │
                   ▼
        MediaPipe Face Mesh
                   │
     ┌─────────────┼─────────────┐
     ▼             ▼             ▼
 Eye Detection  Yawn Detection Head Pose
     │             │             │
     └─────────────┼─────────────┘
                   ▼
            Risk Calculation
                   │
          ┌────────┴────────┐
          ▼                 ▼
   Visual Alerts      Audio Alerts
          │
          ▼
     SQLite Database
          │
          ▼
   Streamlit Dashboard
```

---

# 📊 Driver Risk Levels

| Risk Score | Status |
|------------|---------|
| **0 – 29** | 🟢 Safe |
| **30 – 59** | 🟡 Stay Alert |
| **60 – 74** | 🟠 High Risk |
| **75 – 100** | 🔴 Critical |

---

# 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| Programming | Python |
| Computer Vision | OpenCV, MediaPipe |
| Dashboard | Streamlit, Plotly |
| Database | SQLite |
| Data Processing | NumPy, Pandas |
| Audio Alerts | Pygame |

---


# 📈 Sample Output

During execution, the system continuously displays:

- Eye Aspect Ratio (EAR)
- Mouth Aspect Ratio (MAR)
- Driver Risk Score
- Risk Level
- Driver Safety Score
- Driver Status
- Head Pose
- Break Recommendation

---

# ⚙️ Challenges Faced

- Reducing false yawn detections
- Calibrating EAR and MAR thresholds
- Balancing detection accuracy with real-time performance
- Integrating multiple Computer Vision modules into a single monitoring system
