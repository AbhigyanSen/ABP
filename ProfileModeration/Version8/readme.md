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