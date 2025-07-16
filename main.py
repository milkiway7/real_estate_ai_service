from dotenv import load_dotenv
load_dotenv()
import uvicorn
from fastapi import FastAPI
from Helpers.Logger import get_logger
from EmbeddingPipeline.EmbeddingPipeline import EmbeddingPipeline
from fastapi import HTTPException, status

app = FastAPI()

@app.post("/prepare_to_embedding")
async def prepare_to_embedding():
    get_logger().info("Preparing to embedding")
    try:
        pipeline = EmbeddingPipeline()

        while True:
            items_fetched = await pipeline.run()
            if items_fetched is None or items_fetched < 100:
                get_logger().info("Less than 100 items fetched, stopping the pipeline.")
                break
        return {"status": "success", "message": "Embedding preparation completed successfully."}
    except Exception as e:
        get_logger().error(f"Error during data fetching: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Embedding preparation failed. See logs for details."
        )
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.2", port=8001, reload=False)

