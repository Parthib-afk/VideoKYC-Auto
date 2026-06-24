# VideoKYC-Auto

An Automated Video KYC (Know Your Customer) System built using Flask, OpenCV, EasyOCR, DeepFace, and SQLite.

## Features

* ID Card Upload through Flask Web Application
* OCR-based Text Extraction using EasyOCR
* Face Detection using OpenCV
* Liveness Detection using MediaPipe
* Face Verification using DeepFace
* SQLite Database Storage
* Automated Verification Workflow

## Tech Stack

* Python
* Flask
* OpenCV
* EasyOCR
* DeepFace
* MediaPipe
* SQLite

## Project Workflow

1. Upload ID Card
2. Extract Text using OCR
3. Capture Live Face
4. Perform Liveness Detection
5. Verify Face with ID Photo
6. Store Results in Database
7. Display Verification Status

## Project Structure

VideoKYC-Auto/

* app.py
* ocr.py
* liveness.py
* face_match.py
* database.py
* database.db
* templates/
* uploads/

## Author

Parthib Choudhury
B.Tech CSE, KIIT
