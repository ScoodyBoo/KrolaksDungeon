import uvicorn # Async API Server
import logging
import sys
from api_logic.api_core import app, PORT

if __name__ == "__main__":
    # # Get the root logger
    # root_logger = logging.getLogger()
    # root_logger.setLevel(logging.INFO)

    # # Add a FileHandler to the root logger
    # file_handler = logging.FileHandler("server.log")
    # formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    # file_handler.setFormatter(formatter)
    # root_logger.addHandler(file_handler)

    # # Uvicorn will handle console output by default
    # logging.info("Server Started, logging to server.log")
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=False)