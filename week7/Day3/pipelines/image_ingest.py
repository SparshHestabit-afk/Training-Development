import os
import json
import numpy as np
import faiss
import pytesseract
from PIL import Image
from tqdm import tqdm
from transformers import BlipProcessor, BlipForConditionalGeneration

from src.embeddings.clip_embeddings import CLIPEmbedder

IMAGE_FOLDER = "src/data/raw/images"
VECTOR_PATH = "src/vectorstore/image_index.faiss"
META_PATH = "src/vectorstore/image_metadata.json"


class ImageIngestPipeline:

    def __init__(self):

        print("Initializing pipeline...")

        self.embedder = CLIPEmbedder()

        print("Loading BLIP caption model...")

        self.caption_processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )

        self.caption_model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )

        self.caption_model.eval()

        self.embeddings = []
        self.metadata = []

    def extract_ocr(self, image_path):

        try:
            image = Image.open(image_path)
            return pytesseract.image_to_string(image).strip()
        except:
            return ""

    def generate_caption(self, image_path):

        try:
            image = Image.open(image_path).convert("RGB")

            inputs = self.caption_processor(image, return_tensors="pt")

            output = self.caption_model.generate(**inputs, max_new_tokens=30)

            caption = self.caption_processor.decode(
                output[0], skip_special_tokens=True
            )

            return caption
        except:
            return ""

    def ingest_images(self):

        files = [
            f for f in os.listdir(IMAGE_FOLDER)
            if f.lower().endswith(("png", "jpg", "jpeg"))
        ]

        print(f"\nFound {len(files)} images")

        for idx, file in enumerate(tqdm(files)):

            path = os.path.join(IMAGE_FOLDER, file)

            print(f"\nProcessing: {file}")

            embedding = self.embedder.embed_image(path)

            caption = self.generate_caption(path)

            ocr_text = self.extract_ocr(path)

            self.embeddings.append(embedding)

            self.metadata.append({
                "id": idx,
                "image_path": path,
                "caption": caption,
                "ocr_text": ocr_text
            })

        embeddings = np.array(self.embeddings).astype("float32")

        dim = embeddings.shape[1]

        index = faiss.IndexFlatL2(dim)

        index.add(embeddings)

        os.makedirs("vectorstore", exist_ok=True)

        faiss.write_index(index, VECTOR_PATH)

        with open(META_PATH, "w") as f:
            json.dump(self.metadata, f, indent=2)

        print("\nVector index saved:", VECTOR_PATH)
        print("Metadata saved:", META_PATH)


if __name__ == "__main__":

    pipeline = ImageIngestPipeline()
    pipeline.ingest_images()