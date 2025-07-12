import httpx
from Helpers.Logger import get_logger
import os

class FetchBatch:
    def __init__(self):
        self.data_analysis_url = os.getenv("DATA_ANALYSIS_URL") + "/get_data_for_embedding"
        if not self.data_analysis_url:
            raise ValueError("DATA_ANALYSIS_URL is not set in the environment variables.")
        self.timeout = httpx.Timeout(15.0)
        self.headers = {"Content-Type": "application/json"}
        self.logger = get_logger(self.__class__.__name__)

    async def fetch_batch(self):
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                self.logger.info(f"Starting to fetch data for embedding from {self.data_analysis_url}")
                response = await client.get(self.data_analysis_url, headers=self.headers)
                response.raise_for_status()
                self.logger.info("Data fetched successfully for embedding.")
                return response.json()
            except httpx.RequestError as e:
                self.logger.error(f"An error occurred while fetching data: {e}")
                raise

