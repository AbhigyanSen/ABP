# Face Occlusion Detection - Version 2

## Overview
> Version 2 of the Face Occlusion Detection project introduces significant improvements and changes over Version 1. These enhancements streamline the image processing workflow and improve accuracy in detecting face occlusions. This version now handles image paths instead of URLs across all models, addressing issues related to face cropping and multi-face detection.

## Major Differences from Version 1

### 1. Image Processing Workflow

### Version 1:
- Images were Downloaded and stored in `Images` folder and `TempFaces` folder initially for use in **Face Recognition** _(Part 1)_, **Mediapipe** _(Part 2)_, and **YOLO** _(Part 4)_.
- **CLIP** _(Part 3)_ continued to use **Image URL** for its analysis.

### Version 2:
- Images are first downloaded and stored in `Images` folder and `TempFaces` folder.
- All models (Face Recognition, Mediapipe, YOLO, and CLIP) now use the **Image Path** for analysis.

### 2. Handling of Multiple Faces

### Version 1:
- If `Number of Faces Detected > 1`, it resulted in image rejection due to **Multiple Faces Error**.

### Version 2:
- Recognizes and processes images with only one primary subject in focus.
- Introduces a new function `save_faces` to manage and pass single face images to subsequent models.


## Version 1

```mermaid
graph LR 
A[URL]
A --> B[Images]
B --> C[TempFaces]
C --> D[Mediapipe] -->G
A --> E[CLIP B32] --> G
C --> F[YOLO] --> G
G[Combined Result]  --> H
H[Final Result]

style A fill:#818589,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style B fill:#A9A9A9,stroke:#333,stroke-width:0px,color:#05014a
style G fill:#D3D3D3,stroke:#333,stroke-width:1px,color:#05014a
style C fill:#D3D3D3,stroke:#333,stroke-width:1px,color:#05014a
style D fill:#818589,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style E fill:#818589,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style F fill:#818589,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style H fill:#818589,stroke:#333,stroke-width:0.5px,color:#ddd3d1
```

## Version 2

```mermaid
graph LR 
A[URL]
A --> B[Images]
B --> C[TempFaces]
C --> D[Mediapipe] -->G
C --> E[CLIP B32] --> G
C --> F[YOLO] --> G
G[Combined Result]  --> H
H[Final Result]

style A fill:#5d687e,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style B fill:#869bbb,stroke:#333,stroke-width:0px,color:#05014a
style G fill:#a4b5cd,stroke:#333,stroke-width:1px,color:#05014a
style C fill:#a4b5cd,stroke:#333,stroke-width:1px,color:#05014a
style D fill:#5d687e,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style E fill:#5d687e,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style F fill:#5d687e,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style H fill:#5d687e,stroke:#333,stroke-width:0.5px,color:#ddd3d1
```