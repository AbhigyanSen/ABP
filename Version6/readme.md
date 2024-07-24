The major differences between Version 1 and Version 2 are: <br><br>
**First** <br>
Version 1 first downloaded the images which were used by Face-recognition in Part 1, Mediapipe in Part 2 and YOLO in Part 4. In Part 3, CLIP Model still used to parse the URLs for its Outcome. Hence, in CLIP the ImageURL is passed instead of the Image Path.
In Version 2, the images are first downloaded and the downloaded images are used by all the models including CLIP, as this time, the models take the Image Path insetead of the Image URL. 
<br>
**Second** <br>
In Version 1, if more than 1 face was detected then the Image was said to have Multiple Faces. But, in Version 2, if only 1 subject is in focus diminishing the rest then that image was said to be Single Face and passed onto the next models. Therefore eliminating the Group Photo Factor. *The problem arised here was that, the changes were reflected only in Insight Face and Face-Recognition i.e. in Part 1, but in Part 2 where the Accepted Single Face Image was to be passed to Mediapipe, Face-Recognition had to Crop 1 single Face, but which face to be cropped was a major issue. This problem was solved by creating a new function save_faces and this resulted to passing the Image PAth to the other models instead of the Image URl.



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
    Similar: "https://cdn.abpweddings.com/documents/f1537ddc582e3712654af6a6e2127e88/1707106537072.webp"
