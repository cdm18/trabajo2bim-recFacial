# Facial Recognition System

This project implements a local facial recognition system using Python, `dlib`, and `face_recognition`. It is designed to identify students in images and real-time video.

## Architecture

The solution follows a standard computer vision pipeline:

1.  **Input Acquisition**: Images or Video frames are captured.
2.  **Face Detection**: The system uses Histogram of Oriented Gradients (HOG) (or CNN) to locate faces within the image.
3.  **Feature Extraction**: A 128-dimensional vector (embedding) is computed for each detected face. This encoding represents the unique features of the face.
4.  **Matching**: The system calculates the Euclidean distance between the encoding of the detected face and the database of known student encodings.
    - If the distance is below a threshold (typically 0.6), it is a match.
    - The system selects the match with the most "votes" or smallest distance.
5.  **Output**: The image/frame is annotated with the student's name and a bounding box.

## Setup

1.  **Create and Activate Virtual Environment**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: Installing `dlib` may require CMake and Visual Studio C++ build tools installed on your Windows machine. If you encounter errors, try installing the pre-built wheel for dlib manually or ensure you have the "Desktop development with C++" workload installed in Visual Studio.*

3.  **Prepare Dataset**:
    - Organize student photos in the `dataset/` directory.
    - Create a folder for each student (e.g., `dataset/Juan_Perez/`).
    - Add multiple photos of the student in their respective folder.

## Usage

### 1. Training
Run the training script to generate the face encodings:
```bash
python train_model.py --dataset dataset --encodings encodings.pickle
```
This will create a file named `encodings.pickle` containing the database of known faces.

### 2. Recognition (Video/Webcam)
To start real-time recognition using your webcam:
```bash
python recognize_video.py --encodings encodings.pickle
```
- Press `q` to quit the video window.

### 3. Recognition (Image)
To recognize faces in a specific static image:
```bash
python recognize_image.py --encodings encodings.pickle --image path/to/your/test_image.jpg
```

## Experimentation & Analysis

- **Lighting**: Good lighting improves detection accuracy. Dark environments may lead to missed detections.
- **Pose**: The model is robust to slight head turns but works best with frontal views. Profiles may require the CNN detection method (slower but more accurate).
- **Occlusion**: Glasses or masks can reduce accuracy.
- **Threshold**: The default matching threshold is tuned for general use. Stricter thresholds reduce false positives but might increase false negatives.

## Libraries Used
- **dlib**: Core library for machine learning and face detection.
- **face_recognition**: specific API for simplified face recognition tasks.
- **OpenCV**: Image and video processing.
- **imutils**: Helper functions for image resizing and processing.
