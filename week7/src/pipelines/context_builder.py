import os
import json
import numpy as np
import faiss

class ContextBuilder:

    def __init__(self, max_chars=12000):
        self.max_chars = max_chars

    def build(self, documents):

        context_blocks = []
        total_chars = 0

        for i, doc in enumerate(documents):

            text = doc.get("text", "")
            metadata = doc.get("metadata", {})

            scores = {
                "hybrid_score": doc.get("hybrid_score"),
                "vector_score": doc.get("vector_score"),
                "keyword_score": doc.get("keyword_score"),
                "rerank_score": doc.get("rerank_score")
            }

            if not text:
                continue

            block = (
                f"===== Source {i+1} =====\n"
                f"Text:\n{text}\n\n"
                f"Metadata:\n{metadata}\n\n"
                f"Scores:\n{scores}\n"
                f"------------------------------\n"
            )

            if total_chars + len(block) > self.max_chars:
                break

            context_blocks.append(block)
            total_chars += len(block)

        context = "\n".join(context_blocks)

        return {
            "context": context
        }