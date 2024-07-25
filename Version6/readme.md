# Face Occlusion Detection - Version 6

## Overview
> Version 6 of the Face Occlusion Detection project builds upon the capabilities introduced in Version 5, focusing on improving accuracy and addressing specific scenarios related to face occlusion analysis. This version includes updates to path configurations, error handling, and model confidence thresholds to enhance the overall functionality and reliability of the system.

## Model Configuration Update

##### Version 5:
- The CLIP B32 Model was struggling to differentiate between eyeglasses and sunglasses with thresholding at **0.8**.

##### Version 6:
- The Thresholding was updated from **0.8** to **0.5** to make sure that eyeglasses are parsed by RN101.

Debugging Notes _(Developers)_:
30:  Model Loading Error (Face Analysis)
88:  NSFW Label
151: print(e)                   (deleted)
253: Confidence for CLIP B32
264: RN101 Acceptance 
272: Detected Class for CLIP B32 in 80% Confidence
314: Combined Result 
315: Combined Result
329: Acceptance by RN101        (Eyeglass in CLIP, Sunglass in YOLO)

Error Notes:
If the image is too large like for example "https://cdn.abpweddings.com/documents/7207615415fe2d08eb2dbca0499fae3f/1708077441730.webp?width=150", due to the expansion factor being 30% the program is unable to crop and hence throws ERROR.
Exceptional Case for URL "https://cdn.abpweddings.com/documents/f36cb5718042b66939f7acea8b0420c3/1708156586921.webp", is Accepted. B32 gives a Eyewear Confidence of 45% and Headware Confidence is much lower. If fix is needed then change Confidence at Line 255 in main.py to 0.4.
    Similar:    "https://cdn.abpweddings.com/documents/f1537ddc582e3712654af6a6e2127e88/1707106537072.webp"
                "https://cdn.abpweddings.com/documents/ee7c8ac8283b5f0fb07d1d661016cdaa/1708360968924.webp?width=150?width=150"
