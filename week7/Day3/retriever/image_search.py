import json
import faiss
import numpy as np

from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

from src.embeddings.clip_embeddings import CLIPEmbedder

VECTOR_PATH = "src/vectorstore/image_index.faiss"
META_PATH = "src/vectorstore/image_metadata.json"


class ImageSearch:

    def __init__(self):

        print("Loading vector index...")

        self.index = faiss.read_index(VECTOR_PATH)

        with open(META_PATH) as f:
            self.metadata = json.load(f)

        self.embedder = CLIPEmbedder()
        print("Loading BLIP caption model...")
        self.processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )
        self.caption_model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )

    def search_by_text(self, query, top_k=5):

        embedding = self.embedder.embed_text(query)
        embedding = np.array([embedding]).astype("float32")

        distances, indices = self.index.search(embedding, top_k)

        results = []

        for i in indices[0]:
            results.append(self.metadata[i])

        return results

    def search_by_image(self, image_path, top_k=5):

        embedding = self.embedder.embed_image(image_path)
        embedding = np.array([embedding]).astype("float32")

        distances, indices = self.index.search(embedding, top_k)

        results = []

        for i in indices[0]:
            results.append(self.metadata[i])

        return results
    

    def generate_caption(self, image):

        inputs = self.processor(image, return_tensors="pt")

        output = self.caption_model.generate(**inputs)

        caption = self.processor.decode(output[0], skip_special_tokens=True)

        return caption

if __name__ == "__main__":

    search = ImageSearch()

    results = search.search_by_text("engineering diagram")

    print("\nTop Results\n")

    for r in results:
        print(r["image_path"], r["caption"])