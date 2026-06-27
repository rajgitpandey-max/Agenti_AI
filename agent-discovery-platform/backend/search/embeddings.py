from typing import List
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None

    def load_model(self):
        if self.model is None:
            logger.info(f"Loading embedding model {self.model_name}...")
            # For MVP using a fast local model instead of calling OpenAI API
            self.model = SentenceTransformer(self.model_name)
            logger.info("Model loaded.")

    def embed_text(self, text: str) -> List[float]:
        self.load_model()
        # Returns a 384-dimensional vector for all-MiniLM-L6-v2
        return self.model.encode(text).tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        self.load_model()
        return self.model.encode(texts).tolist()

embedding_service = EmbeddingService()
