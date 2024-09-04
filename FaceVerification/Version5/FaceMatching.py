import insightface
from insightface.app import FaceAnalysis
from io import BytesIO
from PIL import Image
import requests
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import math


try:
    app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
    app.prepare(ctx_id=-1)
except Exception as e:
    print(f"Error loading model: {e}")
    app = None

def getFace(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content)).convert("RGB")
    imagearr = np.asarray(image)
    faces = app.get(imagearr)
    if (len(faces) == 1):
        return faces[0]["embedding"]
    else:
        print("Face count mismatch")
        return None

def compareFace2Aadhar(faceurl,aadharurl):
    faceEmbed = getFace(faceurl)
    aadharEmbed = getFace(aadharurl)
    if(faceEmbed is not None and aadharEmbed is not None):
        similarity = cosine_similarity([faceEmbed],[aadharEmbed])
        percnt = (math.pi - math.acos(similarity)) * 100 / math.pi
        return percnt
    else:
        print("mismatch")
        return None
    
if __name__== "__main__":
    face1_url = "https://im.indiatimes.in/content/2022/Dec/5-copy-28_63a563c0bfd9c.jpg?w=720&h=1280&cc=1&webp=1&q=75"
    face2_url = "https://img.olympics.com/images/image/private/t_16-9_760/f_auto/primary/s0d4s8tbffuvrcmqbhrz"
    print(compareFace2Aadhar(face1_url,face2_url))