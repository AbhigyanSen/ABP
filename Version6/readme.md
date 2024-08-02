# Face Occlusion Detection - Version 6

## Overview
> Version 6 of the Face Occlusion Detection project builds upon the capabilities introduced in Version 5, focusing on improving accuracy and addressing specific scenarios related to face occlusion analysis. This version includes updates to path configurations, error handling, and model confidence thresholds to enhance the overall functionality and reliability of the system.

## Model Configuration Update

### Version 5:
- The **CLIP B32** Model was struggling to differentiate between eyeglasses and sunglasses with thresholding at **0.8**.

### Version 6:
- The Thresholding was updated from **0.8** to **0.5** to make sure that eyeglasses are parsed by **RN101**.

## Debugging Notes _(Developers)_:
- 30:  Model Loading Error        (Face Analysis)
- 88:  NSFW Label
- 151: print(e)                   (deleted)
- 253: Confidence for CLIP B32
- 264: RN101 Acceptance 
- 272: Detected Class for CLIP B32 in 80% Confidence
- 314: Combined Result 
- 315: Combined Result
- 329: Acceptance by RN101        (Eyeglass in CLIP, Sunglass in YOLO)

## Flow Diagram
```mermaid
graph LR
A[Insert URL] --> B[URL Handling]
B --> BA(Image Downloaded) & BB(Error Downloading)
BB --> BC((ERROR)) --> H
BA --> C[Face Detection]
C --> CA(No Face OR Group Face) & CB(Single Face/Single Face in Group)
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

style A fill:#5d687e,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style D fill:#5d687e,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style E fill:#5d687e,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style F fill:#5d687e,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style H fill:#5d687e,stroke:#333,stroke-width:0.5px,color:#ddd3d1

style B fill:#869bbb,stroke:#333,stroke-width:0px,color:#05014a
style BB fill:#ddd3d1,stroke:#333,stroke-width:0.5px,color:#010b19
style DA fill:#ddd3d1,stroke:#333,stroke-width:0.5px,color:#010b19
style DB fill:#869bbb,stroke:#333,stroke-width:0px,color:#05014a
style EA fill:#ddd3d1,stroke:#333,stroke-width:0.5px,color:#010b19
style EE fill:#ddd3d1,stroke:#333,stroke-width:0.5px,color:#010b19
style EB fill:#869bbb,stroke:#333,stroke-width:0px,color:#05014a
style FA fill:#ddd3d1,stroke:#333,stroke-width:0.5px,color:#010b19
style FB fill:#869bbb,stroke:#333,stroke-width:0px,color:#05014a

style G fill:#a4b5cd,stroke:#333,stroke-width:1px,color:#05014a
style C fill:#a4b5cd,stroke:#333,stroke-width:1px,color:#05014a

style BC fill:#ffd3b6,stroke:#333,stroke-width:0.5px,color:#960000
style CC fill:#ffd3b6,stroke:#333,stroke-width:0.5px,color:#960000
style DC fill:#ffd3b6,stroke:#333,stroke-width:0.5px,color:#960000
style EC fill:#ffd3b6,stroke:#333,stroke-width:0.5px,color:#960000
style FC fill:#ffd3b6,stroke:#333,stroke-width:0.5px,color:#960000

style FD fill:#D1FFBD,stroke:#333,stroke-width:0.5px,color:#006400
style ED fill:#D1FFBD,stroke:#333,stroke-width:0.5px,color:#006400
style DD fill:#D1FFBD,stroke:#333,stroke-width:0.5px,color:#006400

style BA fill:#854442,stroke:#333,stroke-width:0.5px,color:#fff4e6
style CB fill:#854442,stroke:#333,stroke-width:0.5px,color:#fff4e6
style CA fill:#854442,stroke:#333,stroke-width:0.5px,color:#fff4e6
```