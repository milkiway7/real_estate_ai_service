from DataClient.FetchBatchClient import FetchBatch
from Helpers.Logger import get_logger

class EmbeddingPipeline:
    def __init__(self):
        self.fetcher = FetchBatch()
        self.logger = get_logger(self.__class__.__name__)

    async def run(self):
        try:
            self.logger.info("Starting embedding pipeline")
            data = await self.fetcher.fetch_batch()
            self.logger.info(f"Data items fetched: {len(data['items'])}")
            # Here you would process the data for embedding
            return len(data['items'])
        except Exception as e:
            self.logger.error(f"Error during embedding pipeline: {e}")
