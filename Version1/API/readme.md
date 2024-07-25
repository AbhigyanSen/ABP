# Face Occlusion Detection API - Version 1

## Overview

Version 1 of the Face Occlusion Detection API integrates the face occlusion detection functionalities into a Flask-based API. This API allows users to submit image URLs for evaluation and receive a final acceptance or rejection decision based on various face occlusion analysis steps.

## Making Requests

To use the Face Occlusion Detection API:

   1. Ensure you have **Postman** installed.


   2. Set up a **POST** request to the API endpoint:
      + URL: http://localhost:5001/process_image
      + Method: 'POST'
      + Body: Select raw and JSON format, then enter the following JSON payload:
        ```sh
        {
            "image_url": "https://example.com/image.jpg"
        }
        ```
        _Replace "https://example.com/image.jpg" with the URL of the image you want to process._


   3. **Send** the Request.
        
    
![image](https://github.com/AbhigyanSen/ABP/assets/62685639/62ee6f05-42ab-41a7-9a7c-17c52f1e8da5)

## Implementation Details

- The API internally uses Python scripts and libraries for various tasks:
- Face Detection and Analysis: Utilizes Insight Face and Face Recognition for face detection and initial analysis.
- Facial Landmark Detection: Uses Mediapipe for detecting facial landmarks.
- Textual Image Analysis: Implements CLIP for analyzing images based on textual descriptions.
- Object Detection: Utilizes YOLO for detecting objects like eyewear and headwear in images.
- For detailed implementation, refer to the demo.py file in the repository.


## Troubleshooting

If you encounter any issues while setting up or using the API, please check the following:
- Ensure all dependencies are installed (requirements.txt).


- Verify the Flask server (app.py) is running on http://localhost:5001.


- Check the input image URL and ensure it points to a valid image file.