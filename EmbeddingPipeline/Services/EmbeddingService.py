from Helpers.Logger import get_logger
from DataClient.EmbeddingClient import EmbeddingClient

class EmbeddingService:
    def __init__(self, data_for_embedding):
        self.logger = get_logger(self.__class__.__name__)
        self.data_for_embedding = data_for_embedding

    async def embed(self):
        try:
            self.logger.info("Starting embedding process")
            # 100 items in data_for_embedding but config on runpod.io is 10 items per batch
            # Split data_for_embedding into chunks of 10 items each and send them to the embedding service on runpod.io 
            # Where model BAAI/bge-m3 will be used for tokenization and embedding
            data_chunks = [self.data_for_embedding[i:i + 10] for i in range(0, len(self.data_for_embedding), 10)]
            self.logger.info(f"Data split into {len(data_chunks)} chunks for embedding")
            embedding_client = EmbeddingClient()
            for chunk in data_chunks:
                embedded_data = await embedding_client.get_embedding(chunk)
                a = 1
        except Exception as e:
            self.logger.error(f"Error during embedding process: {e}")
            raise 
