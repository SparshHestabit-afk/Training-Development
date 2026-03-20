import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer

class RAGEvaluator:
    """
    RAG Evaluation Utility

    Provides:
    - Context match score
    - Faithfulness score
    - Hallucination detection
    - Batch evaluation
    - Debug traces
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        hallucination_threshold: float = 0.35
    ):

        self.model = SentenceTransformer(model_name)
        self.threshold = hallucination_threshold

    # ------------------------------------------------
    # Cosine Similarity
    # ------------------------------------------------

    def _cosine_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:

        denom = (
            np.linalg.norm(emb1) * np.linalg.norm(emb2)
        )

        if denom == 0:
            return 0.0

        return float(np.dot(emb1, emb2) / denom)

    # ------------------------------------------------
    # Embedding Helper
    # ------------------------------------------------

    def _embed(self, text: str) -> np.ndarray:

        if not text or not text.strip():
            return np.zeros(384)

        return self.model.encode(text)

    # ------------------------------------------------
    # Context Match Score
    # ------------------------------------------------

    def context_match_score(self, context: str, query: str) -> float:
        """
        Measures how relevant retrieved context is to query
        """

        context_emb, query_emb = self.model.encode(
            [context, query]
        )

        score = self._cosine_similarity(context_emb, query_emb)

        return round(score, 4)

    # ------------------------------------------------
    # Faithfulness Score
    # ------------------------------------------------

    def faithfulness_score(self, context: str, answer: str) -> float:
        """
        Measures whether answer is grounded in context
        """

        context_emb, answer_emb = self.model.encode(
            [context, answer]
        )

        score = self._cosine_similarity(context_emb, answer_emb)

        return round(score, 4)

    # ------------------------------------------------
    # Hallucination Detection
    # ------------------------------------------------

    def hallucination_check(self, context: str, answer: str) -> Dict:

        score = self.faithfulness_score(context, answer)

        hallucinated = score < self.threshold

        return {
            "hallucinated": hallucinated,
            "faithfulness_score": score,
            "threshold": self.threshold
        }

    # ------------------------------------------------
    # Full Evaluation
    # ------------------------------------------------

    def evaluate(self, query: str, context: str, answer: str) -> Dict:

        context_score = self.context_match_score(context, query)
        faithfulness = self.faithfulness_score(context, answer)
        hallucinated = faithfulness < self.threshold

        return {
            "query": query,
            "context_match_score": context_score,
            "faithfulness_score": faithfulness,
            "hallucinated": hallucinated
        }

    # ------------------------------------------------
    # Batch Evaluation
    # ------------------------------------------------

    def evaluate_batch(
        self,
        records: List[Dict]
    ) -> List[Dict]:
        """
        Evaluate multiple RAG outputs.

        records format:
        [
            {
                "query": "...",
                "context": "...",
                "answer": "..."
            }
        ]
        """

        results = []

        for record in records:

            query = record.get("query", "")
            context = record.get("context", "")
            answer = record.get("answer", "")

            result = self.evaluate(query, context, answer)
            results.append(result)

        return results