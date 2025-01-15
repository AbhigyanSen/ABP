# Face Occlusion Detection - Version 9 (Discarded Version)

## Overview
> Version 9 of the Face Occlusion Detection project introduces significant improvements and optimizations in the image processing pipeline. This update focuses on enhancing image handling (support for base64 image data), refactoring functions for better modularity, and improving model performance for NSFW detection, face cropping, and classification tasks.

## Model Configuration Update

- **Base64 Support:** Image URLs are no longer the only input method; the system can now process base64-encoded images for greater flexibility.
- **Improved Face Detection:** Enhanced algorithms for accurate face detection, ensuring that single and multiple face scenarios are handled effectively.
- **Refined Eyewear Detection:** Integration with CLIP and RN101 models for more accurate classification of eyewear and headwear items such as sunglasses and glasses.
- **NSFW Detection:** The NSFW model is now more tightly integrated into the image processing flow, providing more reliable content moderation.

### Version 8:
- The **input type** is a **Image URL**.
- 'detect_nsfw()' function used OpenCV to load images from disk.
- 'crop_faces()' and 'save_face()' accepts images in form of **NumPy arrays**.

### Version 9:
- Added functionality to handle **base64-encoded image data** in 'base64_to_image()'. This allows for more flexible input options, such as receiving images as base64 strings.
- 'detect_nsfw()' has been updated to process images directly from the PIL image object, allowing for smoother integration with the new base64-to-image pipeline.
- 'crop_faces()' and 'save_face()' functions now directly accept PIL images rather than NumPy arrays, aligning with the image format. 

**Warning:** This is explicitely built for testing if the model handles the use case of Face Occlusion on a 'Gradio' server. Refer to the 'Releases' for the 'Production Version'.

## Flow Diagram
```mermaid
graph LR
A[Insert Base64] --> B[Base64 Handling]
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

style A fill:#c30010,stroke:#333,stroke-width:0.5px,color:#FFDFC8
style D fill:#c30010,stroke:#333,stroke-width:0.5px,color:#FFDFC8
style E fill:#c30010,stroke:#333,stroke-width:0.5px,color:#FFDFC8
style F fill:#c30010,stroke:#333,stroke-width:0.5px,color:#FFDFC8
style H fill:#c30010,stroke:#333,stroke-width:0.5px,color:#FFDFC8

style B fill:#de0a26,stroke:#333,stroke-width:0px,color:#F7D9C4
style BB fill:#FAA080,stroke:#333,stroke-width:0.5px,color:#880808
style DA fill:#FAA080,stroke:#333,stroke-width:0.5px,color:#880808
style DB fill:#de0a26,stroke:#333,stroke-width:0px,color:#F7D9C4
style EA fill:#FAA080,stroke:#333,stroke-width:0.5px,color:#880808
style EE fill:#FAA080,stroke:#333,stroke-width:0.5px,color:#880808
style EB fill:#de0a26,stroke:#333,stroke-width:0px,color:#F7D9C4
style FA fill:#FAA080,stroke:#333,stroke-width:0.5px,color:#880808
style FB fill:#de0a26,stroke:#333,stroke-width:0px,color:#F7D9C4

style G fill:#D2042D,stroke:#333,stroke-width:0px,color:#FFFFFF
style C fill:#D2042D,stroke:#333,stroke-width:0px,color:#FFFFFF

style BC fill:#A52A2A,stroke:#333,stroke-width:1px,color:#F8EDEB
style CC fill:#DC143C,stroke:#333,stroke-width:0.5px,color:#F8EDEB
style DC fill:#DC143C,stroke:#333,stroke-width:0.5px,color:#F8EDEB
style EC fill:#DC143C,stroke:#333,stroke-width:0.5px,color:#F8EDEB
style FC fill:#DC143C,stroke:#333,stroke-width:0.5px,color:#F8EDEB

style FD fill:#E34234,stroke:#333,stroke-width:0.5px,color:#F8EDEB
style ED fill:#E34234,stroke:#333,stroke-width:0.5px,color:#F8EDEB
style DD fill:#E34234,stroke:#333,stroke-width:0.5px,color:#F8EDEB

style BA fill:#ff2c2c,stroke:#333,stroke-width:0.5px,color:#fff4e6
style CB fill:#ff2c2c,stroke:#333,stroke-width:0.5px,color:#fff4e6
style CA fill:#ff2c2c,stroke:#333,stroke-width:0.5px,color:#fff4e6
```