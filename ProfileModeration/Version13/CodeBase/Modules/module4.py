# Module for CLIP-B32 and CLIP-RN101

import torch
import clip
from PIL import Image

# CLIP
device = "cuda" if torch.cuda.is_available() else "cpu"

clip_model, preprocess = clip.load("ViT-B/32", device=device)
text = ["a cap", "a hat", "a sunglass", "a helmet", "a reading glass", "a mask"]
text_tokens = clip.tokenize(text).to(device)

# CLIP RN101 Model
RNmodel, RNpreprocess = clip.load("RN101", device=device)
rn101textlist = ["a sunglass", "a reading glass"]
rn101text = clip.tokenize(rn101textlist).to(device)


# CLIP Processing
def process_image_clip(image):
    try:
        print("(243) CLIP B32 Processing Try")
        image = Image.fromarray(image)  # Converts NumPy array to PIL Image
        B32image = preprocess(image).unsqueeze(0).to(device)  # Converts PIL Image to Tensor
        
        with torch.no_grad():
            logits_per_image, logits_per_text = clip_model(B32image, text_tokens)
            probs = logits_per_image.softmax(dim=-1).cpu().numpy()
        
        predicted_index = probs.argmax()
        confidence = probs[0][predicted_index]
        detected_class = text[predicted_index]
        print(f"\nB32 Detected Class: {detected_class} and Confidence: {confidence}\n")
        
        if confidence > 0.5 and (detected_class == "a sunglass" or detected_class == "a reading glass"):            
            if detected_class in ["a sunglass", "a reading glass"]:
                print("(258) CLIP RN101 Processing Try")

                with torch.no_grad():
                    rn101_logits_per_image, rn101_logits_per_text = RNmodel(B32image, rn101text)
                    rn101_probs = rn101_logits_per_image.softmax(dim=-1).cpu().numpy()
                rn101_predicted_index = rn101_probs.argmax()
                rn101_confidence = rn101_probs[0][rn101_predicted_index]
                RNdetected_class = rn101textlist[rn101_predicted_index]
                print(f"\nRN101 Confidence: {rn101_confidence} Predicted Class RN101: {RNdetected_class}\n")

                if rn101_confidence > 0.5 and rn101textlist[rn101_predicted_index] == "a reading glass":
                    print("Accepted by RN101 for Eyeglasses")
                    return "Accepted", None, confidence, detected_class
                else:
                    return "Rejected", f"Error: {detected_class}", confidence, detected_class
            else:
                return "Rejected", f"Error: {detected_class}", confidence, detected_class
        
        elif confidence > 0.8:                                                              # Rejection for Headware
            return "Rejected", f"Error: {detected_class}", confidence, detected_class
        
        else:
            return "Accepted", None, confidence, detected_class
        
    except Exception as e:
        print("(282) CLIP Processing Exception")
        return 'Rejected', str(e), 0, None