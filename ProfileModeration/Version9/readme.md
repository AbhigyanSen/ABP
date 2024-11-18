# Face Occlusion Detection - Version 9 (Dummy Version)

## Overview
> Version 9 of the Face Occlusion Detection project introduces significant improvements and optimizations in the image processing pipeline. This update focuses on enhancing image handling (support for base64 image data), refactoring functions for better modularity, and improving model performance for NSFW detection, face cropping, and classification tasks.

Is discarded due to not detecting faces properly.

## Model Configuration Update:

### Version 8:
- The **input type** is a **Image URL**.
- 'detect_nsfw()' function used OpenCV to load images from disk.
- 'crop_faces()' and 'save_face()' accepts images in form of **NumPy arrays**.

### Version 9:
- Added functionality to handle **base64-encoded image data** in 'base64_to_image()'. This allows for more flexible input options, such as receiving images as base64 strings.
- 'detect_nsfw()' has been updated to process images directly from the PIL image object, allowing for smoother integration with the new base64-to-image pipeline.
- 'crop_faces()' and 'save_face()' functions now directly accept PIL images rather than NumPy arrays, aligning with the image format. 

## Flow Diagram
```mermaid
graph LR
A[Base64] --> B[Handling Base64]
B --> BA(Image Downloaded) & BB(Error Downloading)
BB --> BC((ERROR)) --> H
BA --> C[Face Detection]
C --> CA(No Face OR Group Face) & CB(Single Face OR Largest Face in Group)
CA --> CC((REJECT)) --> H
CB --> D[Mediapipe]
D --> DA(Top/Bottom Face Error) & DB(No Error)
DA --> DC((REJECT)) --> G
DB --> DD((ACCEPT)) --> G
CB --> E[CLIP B32]
E --> EA(Presence of Eyewear/Headware) & EB(Eyewear/Headwear Absent)
EA -- SUNGLASSES/EYEGLASSES --> EE[CLIP RN101] 
EC((REJECT))
EE -- SUNGLASSES --> EC --> G
EE -- EYEGLASSES --> ED
EB --> ED((ACCEPT)) --> G
CB --> F[YOLO]
F --> FA(Presence of Eyewear/Headware) & FB(Eyewear/Headwear Absent)
FA --> FC((REJECT)) --> G
FB --> FD((ACCEPT)) --> G
G[Combined Result] --> H
H[Final Result]

style A fill:#c30010,stroke:#333,stroke-width:0.5px,color:#F5F5DC
style D fill:#c30010,stroke:#333,stroke-width:0.5px,color:#F5F5DC
style E fill:#c30010,stroke:#333,stroke-width:0.5px,color:#F5F5DC
style F fill:#c30010,stroke:#333,stroke-width:0.5px,color:#F5F5DC
style H fill:#c30010,stroke:#333,stroke-width:0.5px,color:#F5F5DC

style B fill:#de0a26,stroke:#333,stroke-width:0px,color:#FFF8DC
style BB fill:#ffcbd1,stroke:#333,stroke-width:0.5px,color:#c30010
style DA fill:#ffcbd1,stroke:#333,stroke-width:0.5px,color:#c30010
style DB fill:#de0a26,stroke:#333,stroke-width:0px,color:#FFF8DC
style EA fill:#ffcbd1,stroke:#333,stroke-width:0.5px,color:#c30010
style EE fill:#ffcbd1,stroke:#333,stroke-width:0.5px,color:#c30010
style EB fill:#de0a26,stroke:#333,stroke-width:0px,color:#FFF8DC
style FA fill:#ffcbd1,stroke:#333,stroke-width:0.5px,color:#c30010
style FB fill:#de0a26,stroke:#333,stroke-width:0px,color:#FFF8DC

style G fill:#ee6b6e,stroke:#333,stroke-width:0px,color:#FFFFFF
style C fill:#ee6b6e,stroke:#333,stroke-width:0px,color:#FFFFFF

style BC fill:#ffd3b6,stroke:#333,stroke-width:0.5px,color:#960000
style CC fill:#ffd3b6,stroke:#333,stroke-width:0.5px,color:#960000
style DC fill:#ffd3b6,stroke:#333,stroke-width:0.5px,color:#960000
style EC fill:#ffd3b6,stroke:#333,stroke-width:0.5px,color:#960000
style FC fill:#ffd3b6,stroke:#333,stroke-width:0.5px,color:#960000

style FD fill:#D1FFBD,stroke:#333,stroke-width:0.5px,color:#006400
style ED fill:#D1FFBD,stroke:#333,stroke-width:0.5px,color:#006400
style DD fill:#D1FFBD,stroke:#333,stroke-width:0.5px,color:#006400

style BA fill:#ff2c2c,stroke:#333,stroke-width:0.5px,color:#fff4e6
style CB fill:#ff2c2c,stroke:#333,stroke-width:0.5px,color:#fff4e6
style CA fill:#ff2c2c,stroke:#333,stroke-width:0.5px,color:#fff4e6
```