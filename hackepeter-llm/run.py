import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.endpoints import router
from src.utils.utils import initialize_graph

app = FastAPI()

# Configure CORS middleware to allow all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(router)

if __name__ == "__main__":
    # TODO - Uncomment the following lines to create the graph file
    initialize_graph()

    uvicorn.run(app, host="0.0.0.0", port=8000)


