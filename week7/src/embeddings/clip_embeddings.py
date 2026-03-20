import clip
import torch
import numpy as np
from PIL import Image


class CLIPEmbedder:

    def __init__(self):

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print("Loading CLIP model...")

        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)

    def embed_image(self, image_path):

        image = self.preprocess(Image.open(image_path)).unsqueeze(0).to(self.device)

        with torch.no_grad():
            features = self.model.encode_image(image)

        features = features / features.norm(dim=-1, keepdim=True)

        return features.cpu().numpy()[0].astype("float32")

    def embed_text(self, text):

        tokens = clip.tokenize([text]).to(self.device)

        with torch.no_grad():
            features = self.model.encode_text(tokens)

        features = features / features.norm(dim=-1, keepdim=True)

        return features.cpu().numpy()[0].astype("float32")