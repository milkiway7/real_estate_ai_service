from dotenv import load_dotenv
load_dotenv()
import uvicorn
from fastapi import FastAPI
from Helpers.Logger import get_logger
from DataClient.FetchBatchClient import FetchBatch

app = FastAPI()


@app.post("/prepare_to_embedding")
async def prepare_to_embedding():
    get_logger().info("Preparing to embedding")
    try:
        # send http request to the data_agent to get the data do it in while loop and finish when data is < 100
        fetcher = FetchBatch()
        data = await fetcher.fetch_batch()
        get_logger().info(f"Data: {data}")
    except Exception as e:
        get_logger().error(f"Error during data fetching: {e}")
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.2", port=8001, reload=False)

