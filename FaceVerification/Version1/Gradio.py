import gradio as gr
import insightface
from insightface.app import FaceAnalysis
from io import BytesIO
from PIL import Image
import requests
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import math

# Initialize the FaceAnalysis model
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
    if len(faces) == 1:
        return faces[0]["embedding"]
    else:
        print("Face count mismatch")
        return None

def compareFace2Aadhar(faceurl, aadharurl):
    faceEmbed = getFace(faceurl)
    aadharEmbed = getFace(aadharurl)
    if faceEmbed is not None and aadharEmbed is not None:
        similarity = cosine_similarity([faceEmbed], [aadharEmbed])
        percnt = (math.pi - math.acos(similarity[0][0])) * 100 / math.pi
        return percnt
    else:
        print("Mismatch")
        return 0

def process_images(face_url, aadhar_url):
    # Fetch and display images
    face_image = Image.open(BytesIO(requests.get(face_url).content)).convert("RGB")
    aadhar_image = Image.open(BytesIO(requests.get(aadhar_url).content)).convert("RGB")
    
    # Calculate similarity
    percentage = compareFace2Aadhar(face_url, aadhar_url)
    
    return face_image, aadhar_image, percentage

# Define Gradio interface
iface = gr.Interface(
    fn=process_images,
    inputs=[
        gr.Textbox(label="Face Image URL"),
        gr.Textbox(label="Aadhar Image URL")
    ],
    outputs=[
        gr.Image(type="pil", label="Face Image"),
        gr.Image(type="pil", label="Aadhar Image"),
        gr.Textbox(label="Similarity Percentage")
    ],
    title="Face Similarity Comparison",
    description="Enter URLs of two images to compare their face similarity."
)

# Launch the interface
iface.launch()