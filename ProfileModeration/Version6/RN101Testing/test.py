import torch
import clip
from PIL import Image
import numpy as np

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("RN101", device=device)

image = preprocess(Image.open("/home/abp/Documents/ABPProduction/ABP/Version5/RN101Testing/download.jpeg")).unsqueeze(0).to(device)
lst = ["a sunglass", "a reading glass"]
text = clip.tokenize(lst).to(device)

with torch.no_grad():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text)
    
    logits_per_image, logits_per_text = model(image, text)
    probs = logits_per_image.softmax(dim=-1).cpu().numpy()

print("Label probs:", probs)  
print(lst[np.argmax(probs[0])])