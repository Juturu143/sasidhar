# Automatic Number Plate Recognition (ANPR) System

An Automatic Number Plate Recognition (ANPR) system developed using **YOLO11, PaddleOCR, OpenCV, Python, and MySQL/XAMPP**.

The system detects vehicle number plates from a video stream, tracks detected objects, checks whether they enter a predefined Region of Interest (ROI), extracts the number plate region, reads the plate text using OCR, and stores the detected number plate along with the entry date and time in a MySQL database.

---

## 📌 Project Overview

Automatic Number Plate Recognition is a computer vision application used to automatically detect and read vehicle registration numbers.

This project combines:

- **YOLO11** for number plate detection and tracking
- **OpenCV** for video processing and image operations
- **PaddleOCR** for extracting text from detected number plates
- **MySQL** for storing detected plate information
- **XAMPP** for running the local MySQL database
- **CVZone** for displaying information on the video
- **Python** as the main programming language

---

## 🎯 Objectives

The main objectives of this project are:

1. Detect number plates from vehicle video footage.
2. Track detected objects using YOLO11.
3. Identify vehicles entering a predefined Region of Interest.
4. Crop the detected number plate.
5. Extract the registration number using PaddleOCR.
6. Clean the OCR output.
7. Store the detected number plate in a MySQL database.
8. Record the date and time of the vehicle entry.

---

## ✨ Features

- YOLO11-based number plate detection
- Object tracking using tracking IDs
- Region of Interest (ROI) based detection
- Automatic number plate cropping
- Optical Character Recognition (OCR)
- OCR text cleaning
- Automatic MySQL database creation
- Automatic table creation
- Vehicle entry date and time storage
- Duplicate tracking-ID prevention
- Real-time video processing

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| YOLO11 | Number plate detection and tracking |
| TensorFlow Lite | Model format used by the detection model |
| OpenCV | Video and image processing |
| PaddleOCR | Number plate text recognition |
| NumPy | Array and ROI operations |
| CVZone | Displaying information on the video |
| MySQL | Database for storing plate records |
| XAMPP | Local MySQL server environment |

---

## 🧠 System Architecture

```text
                    Input Video
                         |
                         v
                   YOLO11 Model
                         |
                         v
              Number Plate Detection
                         |
                         v
                  Object Tracking
                         |
                         v
                  ROI Verification
                         |
                         v
                 Crop Number Plate
                         |
                         v
                    PaddleOCR
                         |
                         v
                  OCR Text Cleaning
                         |
                         v
                    MySQL Database
                         |
                         v
              Plate + Date + Time
