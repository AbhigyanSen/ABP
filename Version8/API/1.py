import requests
import cv2
import numpy as np
from insightface.app import FaceAnalysis

def get_face_detection_confidence(image_url):
    # Download the image from the URL
    response = requests.get(image_url)
    image = np.frombuffer(response.content, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # Initialize the FaceAnalysis model
    app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])  # Add providers based on your setup
    app.prepare(ctx_id=0, det_size=(640, 640))  # Set det_size according to your image size

    # Detect faces in the image
    faces = app.get(image)

    # If faces are detected, return the confidence score
    if faces:
        return [face.det_score for face in faces]
    else:
        return "No faces detected"

# Example usage:
image_url = "https://img.freepik.com/premium-photo/young-handsome-man-smiling-cheerfully-feeling-happy-showing-concept-motorbike-helmet-concept_1194-360385.jpg"
confidence_scores = get_face_detection_confidence(image_url)
print(confidence_scores)