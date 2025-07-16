from DataClient.FetchBatchClient import FetchBatch
from Helpers.Logger import get_logger
from EmbeddingPipeline.Services.PrepareDataForEmbeddingService import PrepareDataForEmbeddingService
from DataClient.EmbeddingClient import EmbeddingClient

class EmbeddingPipeline:
    def __init__(self):
        self.fetcher = FetchBatch()
        self.prepare_data_service = PrepareDataForEmbeddingService()
        self.logger = get_logger(self.__class__.__name__)
        self.fetched_data = None
        self.embedding_count = 0

    async def run(self):
        try:
            self.logger.info("Starting embedding pipeline")
            data = await self.fetcher.fetch_batch()
            self.fetched_data = data['items']
            self.logger.info(f"Data items fetched: {len(self.fetched_data)}")
            if not self.fetched_data:
                self.logger.info("No items fetched, stopping the pipeline.")
                return 0
            # Prepare data for embedding (make one string from all items)
            self.logger.info("Joining texts for embedding")
            data_for_embedding = self.prepare_data_service.build_text(self.fetched_data)
            if not data_for_embedding:
                self.logger.info("No data prepared for embedding, stopping the pipeline.")
                return 0
            # Tokenizer & embedding with BAAI/bge-m3 on runpod.io
            self.logger.info("Starting embedding process")
            embedding_client = EmbeddingClient()
            embeddings = await embedding_client.get_embedding(data_for_embedding)
            self.embedding_count += len(embeddings)
            self.logger.info(f"Embeddings received: {self.embedding_count} items")
            # Save to qudrant
            self.logger.info("Embedding pipeline completed successfully")
            return len(self.fetched_data)
        except Exception as e:
            self.logger.error(f"Error during embedding pipeline: {e}")
