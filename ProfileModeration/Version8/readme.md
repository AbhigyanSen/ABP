# Face Occlusion Detection - Version 8 (Dummy Version)

## Overview
> Version 8 of the Face Occlusion Detection project builds upon the capabilities introduced in Version 7, focusing on maintaining same functionalities along with addressing specific scenarios related to face occlusion analysis. This version includes handling of the Temporary Folders being deleted after successful execution of the code.

## Model Configuration Update

### Version 7:
- The temporary folders 'Images', 'TempFaces' were not being deleted.

### Version 8:
- The temporary folders 'Images', 'TempFaces' were are now being deleted.
- The problem was due to making of the 'Images' folder outside of the Working Directory and providing the Relative Path in the Code.

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