# Profile Moderation System - Version 10 (Gradio Testing)

## Overview
> Version 10 of the Profile Moderation System integrates advanced image processing techniques and AI models for image validation and testing it using Gradio. This version introduces improved modularity and enhanced performance for NSFW detection, face cropping, eyewear detection, and object classification. It supports image URLs, base64-encoded image data, and provides a seamless experience in moderating profile images.

## Model Configuration Update

- **Base64 Support:** Image URLs are no longer the only input method; the system can now process base64-encoded images for greater flexibility.
- **Improved Face Detection:** Enhanced algorithms for accurate face detection, ensuring that single and multiple face scenarios are handled effectively.
- **Refined Eyewear Detection:** Integration with CLIP and RN101 models for more accurate classification of eyewear and headwear items such as sunglasses and glasses.
- **NSFW Detection:** The NSFW model is now more tightly integrated into the image processing flow, providing more reliable content moderation.

### Version 9:
- The input type is a Image URL.
- The system used OpenCV for loading images from the URL and PIL for face cropping.
- NSFW detection was performed using a pre-trained ViT-based model.

### Version 10:
- **Input Types: Supports both Image URL and Base64-encoded Image Data.
- **Face Detection:** Refined face detection using InsightFace and MediaPipe.
- **Face Cropping:** Direct image handling with PIL images instead of NumPy arrays for better compatibility.
- **Eyewear and Headwear Detection:** Uses CLIP and RN101 models for classifying eyewear and headwear.
- **NSFW Content Detection:** Enhanced workflow using a more efficient method for NSFW classification using the Vision Transformer (ViT) model.

**Warning:** This is explicitely built for testing if the model handles the use case of Face Occlusion on a 'Gradio' server. Refer to the 'Releases' for the 'Production Version'.

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