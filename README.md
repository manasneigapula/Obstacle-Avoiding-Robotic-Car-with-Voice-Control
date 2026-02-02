
# 🚗 Obstacle Avoiding Robotic Car with Voice Control (Raspberry Pi)

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-4B-c51a4a?logo=raspberrypi)
![Platform](https://img.shields.io/badge/Platform-Robotics-green)
![OS](https://img.shields.io/badge/OS-Raspberry%20Pi%20OS-lightgrey?logo=linux)
![Status](https://img.shields.io/badge/Status-Completed-success)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Voice Control](https://img.shields.io/badge/Feature-Voice%20Control-blueviolet)

A semi-autonomous, voice-activated robotic car built using **Raspberry Pi 4B**, designed to intelligently navigate obstacles while remaining continuously responsive to user voice commands. The system uses a **non-blocking, multithreaded architecture** to ensure real-time decision-making, safe human interaction, and hands-free control.

---

## 📌 Project Overview

Traditional beginner robots suffer from blocking architectures that make them unresponsive while executing tasks. This project overcomes that limitation by implementing **parallel processing**, allowing the robot to:

- Continuously listen for voice commands  
- Autonomously navigate environments  
- Detect human presence and trigger safety protocols  
- Make informed path decisions using active scanning  

The robot functions as a **standalone device**, automatically starting on power-up and operating without external controllers.

---

## 🎯 Objectives

- Implement **non-blocking, multithreaded control**
- Enable **voice-based activation and deactivation**
- Perform **intelligent obstacle avoidance** using active scanning
- Ensure **human-aware safety** using PIR motion detection
- Achieve **fully autonomous boot and operation**

---

## 🧠 Key Features

- 🎙️ Voice control using USB microphone  
- 🧵 Multithreaded Python architecture  
- 📡 Ultrasonic sensor with servo-based scanning  
- 🧍 PIR sensor for human detection & safety override  
- 🤖 Intelligent path selection (left/right scan)  
- 🔄 Auto-start on boot using cron jobs  

---

## 🛠️ Hardware Components

- Raspberry Pi 4B  
- L298N Motor Driver  
- HC-SR04 Ultrasonic Sensor  
- SG90 Micro Servo Motor  
- PIR Motion Sensor  
- USB Microphone  
- 2WD Robot Chassis  
- Dual Power Supply (Pi + Motors)

---

## 🧩 Software Stack

- **Language:** Python 3  
- **OS:** Raspberry Pi OS  
- **Libraries Used:**
  - RPi.GPIO
  - speech_recognition
  - threading
  - time

---

## ⚙️ System Architecture

### Control Logic Priority
1. Voice command listener (background thread)
2. PIR human detection (highest priority interrupt)
3. Ultrasonic obstacle detection
4. Servo-based environment scanning
5. Motor control execution

A global state variable (`car_running`) enables instant start/stop functionality through voice commands.

---

## 🔌 Power Architecture

- Raspberry Pi powered via **5V USB power bank**
- Motors powered via **separate battery pack**
- **Common ground** shared across all components for signal integrity

---

## 🧪 Testing & Results

- Accurate voice recognition in moderate noise
- Immediate response to stop commands during motion
- Reliable obstacle detection and avoidance
- Successful human-aware safety override
- Consistent autonomous startup across power cycles

---

## 🌍 Real-World Applications

- Assistive robots for indoor mobility support  
- Educational robotics platform  
- Automated indoor logistics (labs, offices)  
- Interactive robotic toys or demos  

---

## 🚀 Future Enhancements

- SLAM-based environment mapping  
- Offline voice recognition  
- Expanded voice command set  
- Camera or LiDAR integration  

---

## 👨‍💻 Author 

- **Manas Krishna Neigapula** 


