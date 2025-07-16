from Helpers.Logger import get_logger
import httpx
import os
from fastapi import HTTPException
import asyncio

class EmbeddingClient:
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self.baai_bge_m3_url = os.getenv("BAAI_BGE_M3_URL")
        if not self.baai_bge_m3_url:
            raise ValueError("BAAI_BGE_M3_URL is not set in the environment variables.")
        self.timeout = httpx.Timeout(30.0)
        self.headers = {"Content-Type": "application/json",
                        "Authorization": f"Bearer {os.getenv('RUNPOD_API_KEY')}"}
    
    async def get_embedding(self,data_for_embedding):   
        try:
            task_id = await self.send_data_get_task_id(data_for_embedding)
            embeddings = await self.get_embedding_result(task_id)
            return embeddings
        except httpx.HTTPStatusError as e:
            self.logger.error(f"HTTP error occurred in get_embedding: {e.response.status_code} - {e.response.text}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Embedding service error: {e.response.status_code} - {e.response.text}"
            )
        
    async def send_data_get_task_id(self, data_for_embedding):
        try:
            self.logger.info("Start sending text data for embedding")
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    (f"{self.baai_bge_m3_url}/run"),
                    json={
                        "input": 
                            {
                            "input": data_for_embedding
                            }
                    },
                    headers=self.headers
                )
                response.raise_for_status()
                self.logger.info("Text data successfully sent for embedding")
                response_data = response.json()
                return response_data["id"]
        except httpx.HTTPStatusError as e:
            self.logger.error(f"HTTP error occurred in send_data_get_task_id: {e.response.status_code} - {e.response.text}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Embedding service error: {e.response.status_code} - {e.response.text}"
            )
        
    async def get_embedding_result(self, task_id):
        try:
            self.logger.info(f"Fetching embedding result for task ID: {task_id}")
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                for attempt in range(30):
                    response = await client.get(
                        f"{self.baai_bge_m3_url}/status/{task_id}",
                        headers=self.headers
                    )
                    response.raise_for_status()
                    data = response.json()
                    status = data.get("status")
                    if status == "COMPLETED":
                        self.logger.info("Embedding result fetched successfully")
                        return data["output"]["data"]
                    elif status == "FAILED":
                        self.logger.error(f"Embedding task failed: {status}")
                        raise HTTPException(
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Embedding task {status.lower()}"
                        )   
                    await asyncio.sleep(5)
                raise TimeoutError("Embedding task timed out after 30 attempts")
        except httpx.HTTPStatusError as e:
            self.logger.error(f"HTTP error occurred in get_embedding_result: {e.response.status_code} - {e.response.text}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Embedding service error: {e.response.status_code} - {e.response.text}"
            )
