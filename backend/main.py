from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from constants import SERVER_URL, PORT, ENV
from apps.calculator import router as calculator_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def root():
    return {"message": "Server is running"}


# Include router for calculator functionality
app.include_router(calculator_router, tags=["calculate"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=SERVER_URL, port=int(PORT), reload=(ENV == "dev")
    )
