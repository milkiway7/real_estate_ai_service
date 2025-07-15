from Helpers import get_logger
import httpx
import os

class EmbeddingClient:
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self.baai_bge_m3_url = os.getenv("BAAI_BGE_M3_URL")
        if not self.baai_bge_m3_url:
            raise ValueError("BAAI_BGE_M3_URL is not set in the environment variables.")