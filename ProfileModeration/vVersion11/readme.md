# Face Occlusion Detection - Version 11


## Overview
> Version 11 of the Face Occlusion Detection project enhances the image processing pipeline with the addition of advanced models, more robust face detection techniques, and refined decision-making processes. The system is designed to detect occlusions and various object classifications (such as eyewear and headwear) while ensuring high accuracy with multiple model integrations.

## Model Configuration Update
- **Streamlining the Process** Adding log statements for checkpoint visualization.
- **Log File Modifications** Modifying the log file for debugging.

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
'''