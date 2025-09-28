from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import health, books, scraping
from config.settings import settings
from utils.logger import setup_logging
import logging

logger = setup_logging()
logger.info("Starting Backend API")

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    debug=settings.DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(books.router, prefix="/api/v1", tags=["books"])
app.include_router(scraping.router, prefix="/api/v1", tags=["scraping"])

@app.get("/")
async def root():
    return {"message": settings.API_TITLE, "version": settings.API_VERSION}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)