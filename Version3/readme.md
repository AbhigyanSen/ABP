# Face Occlusion Detection - Version 3

## Overview
> Version 3 of the Face Occlusion Detection project builds upon the advancements of Version 2 with targeted improvements to enhance accuracy and refine the handling of specific occlusion types. This version introduces nuanced changes in the decision-making process to better classify images based on detected eyeglasses, addressing previous discrepancies.

## Eyewear Classification Enhancement

##### Version 2:
- Images were **Rejected** if **YOLO** detect any of the classes.

##### Version 3:
- In **YOLO**, if the detected class was `eyeglasses`, then the Image was **Accepted**.

## Seamless Path Updation for Server Deployment

##### Version 2:
- While deploying the model on the server finally, certain path changes `yolo_model` and `base_folder` were necessary. It was combursome to solve them.

##### Version 3:
- Now both the paths can be updated seamlessly via `YOLO_FOLDER` and `BASE_FOLDER`.


## Version 2

```mermaid
graph LR 
A[YOLO] -- NO CLASS DETECTED --> B((ACCEPT))
A[YOLO] -- ANY CLASS DETECTED --> C((REJECT))

style A fill:#818589,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style B fill:#A9A9A9,stroke:#333,stroke-width:0px,color:#05014a
style C fill:#D3D3D3,stroke:#333,stroke-width:1px,color:#05014a
```

## Version 3

```mermaid
graph LR 
A[YOLO] -- NO CLASS/EYEGLASSES DETECTED --> B((ACCEPT))
A[YOLO] -- ANY CLASS EXCEPT EYEGLASSES DETECTED  --> C((REJECT))

style A fill:#5d687e,stroke:#333,stroke-width:0.5px,color:#ddd3d1
style C fill:#ffd3b6,stroke:#333,stroke-width:0.5px,color:#960000
style B fill:#D1FFBD,stroke:#333,stroke-width:0.5px,color:#006400
```