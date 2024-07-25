# Face Occlusion Detection - Version 4

## Overview
> Version 4 of the Face Occlusion Detection project introduces a new model integration from Falcon AI to enhance image classification capabilities. This version focuses on improving the filtering process by directly rejecting images classified as Not Safe For Work (NSFW), thus optimizing the workflow and ensuring content appropriateness.

## Integration of NSFW Detection Model

##### Version 3:
- No Obscence Images were **Rejected**.

##### Version 4:
- If any obscene image was found, it will be **Rejected** _(in part 1)_ now and not processed further.


## Version 3

```mermaid
graph LR 
A[Images]
A --> I[Face Analysis & Face Recognition] 
I --> D[Mediapipe] -->G
I --> E[CLIP B32] --> G
I --> F[YOLO] --> G
G[Combined Result]  --> H
H[Final Result]

style A fill:#818589,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style I fill:#D3D3D3,stroke:#333,stroke-width:1px,color:#05014a
style G fill:#D3D3D3,stroke:#333,stroke-width:1px,color:#05014a
style D fill:#818589,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style E fill:#818589,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style F fill:#818589,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style H fill:#818589,stroke:#333,stroke-width:0.5px,color:#ddd3d1
```

## Version 4

```mermaid
graph LR 
A[Images]
A --> C[NSFW]
C -- Normal --> I[Face Analysis & Face Recognition] 
C -- NSFW --> J((REJECT))
I --> D[Mediapipe] -->G
I --> E[CLIP B32] --> G
I --> F[YOLO] --> G
G[Combined Result]  --> H
J--> H[Final Result]

style A fill:#5d687e,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style I fill:#a4b5cd,stroke:#333,stroke-width:1px,color:#05014a
style G fill:#a4b5cd,stroke:#333,stroke-width:1px,color:#05014a
style C fill:#869bbb,stroke:#333,stroke-width:0px,color:#05014a
style D fill:#5d687e,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style E fill:#5d687e,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style F fill:#5d687e,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style H fill:#5d687e,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style J fill:#ffd3b6,stroke:#333,stroke-width:0.5px,color:#960000
```