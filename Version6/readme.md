The major differences between Version 1 and Version 2 are: <br><br>
**First** <br>
Version 1 first downloaded the images which were used by Face-recognition in Part 1, Mediapipe in Part 2 and YOLO in Part 4. In Part 3, CLIP Model still used to parse the URLs for its Outcome. Hence, in CLIP the ImageURL is passed instead of the Image Path.
In Version 2, the images are first downloaded and the downloaded images are used by all the models including CLIP, as this time, the models take the Image Path insetead of the Image URL. 
<br>
**Second** <br>
In Version 1, if more than 1 face was detected then the Image was said to have Multiple Faces. But, in Version 2, if only 1 subject is in focus diminishing the rest then that image was said to be Single Face and passed onto the next models. Therefore eliminating the Group Photo Factor. *The problem arised here was that, the changes were reflected only in Insight Face and Face-Recognition i.e. in Part 1, but in Part 2 where the Accepted Single Face Image was to be passed to Mediapipe, Face-Recognition had to Crop 1 single Face, but which face to be cropped was a major issue. This problem was solved by creating a new function save_faces and this resulted to passing the Image PAth to the other models instead of the Image URl.
