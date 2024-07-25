# Face Occlusion Detection - Version 3

## Overview
> Version 5 of the Face Occlusion Detection project introduces the RN101 model for enhanced classification between eyeglasses and sunglasses. This version aims to improve accuracy in identifying specific types of occlusions, thereby refining the decision-making process for image acceptance or rejection

## Integration of RN101 Model

##### Version 4:
- The CLIP B32 Model was struggling to differentiate between eyeglasses and sunglasses and hence **Rejected** eyeglasses.

##### Version 5:
- A new check was implemented by adding RN101 to confirm the presence of eyeglasses. Hence, there was an imporvement in parsing sunjects wearing eyeglasses.


## Version 4

```mermaid
graph LR 
I[Face Analysis & Face Recognition] 
I --> D[Mediapipe] -->G
I --> E[CLIP B32] --> G
I --> F[YOLO] --> G
G[Combined Result]  --> H
H[Final Result]

style I fill:#D3D3D3,stroke:#333,stroke-width:1px,color:#05014a
style G fill:#D3D3D3,stroke:#333,stroke-width:1px,color:#05014a
style D fill:#818589,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style E fill:#818589,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style F fill:#818589,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style H fill:#818589,stroke:#333,stroke-width:0.5px,color:#ddd3d1
```

## Version 5
```mermaid
graph LR 
I[Image Analysis] 
I --> D[Mediapipe] --> G
I --> E[CLIP B32] -- SUNGLASS --> A[CLIP RN101] -- SUNGLASS --> J((REJECT)) --> G
A[CLIP RN101] -- EYEGLASSES --> K((ACCEPT)) --> G
E -- ANY CLASS EXCEPT SUNGLASS --> J
E -- NO CLASS --> K
I --> F[YOLO] --> G
G[Combined Result]  --> H
H[Final Result]

style I fill:#a4b5cd,stroke:#333,stroke-width:1px,color:#05014a
style G fill:#a4b5cd,stroke:#333,stroke-width:1px,color:#05014a
style D fill:#5d687e,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style E fill:#5d687e,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style F fill:#5d687e,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style H fill:#5d687e,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style A fill:#869bbb,stroke:#333,stroke-width:0px,color:#05014a
style J fill:#ffd3b6,stroke:#333,stroke-width:0.5px,color:#960000
style K fill:#D1FFBD,stroke:#333,stroke-width:0.5px,color:#006400
```