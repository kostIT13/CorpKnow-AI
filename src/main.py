import logging
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.core.database import engine 
from sqlalchemy import text 
from src.core.logging_settings import setup_logging
from src.api.auth.endpoints import router as auth_router


setup_logging(level=os.getenv("LOG_LEVEL", "INFO"))

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Приложение запущено")
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(f"Ошибка подключения к бд:{e}")
    yield
    
    await engine.dispose() 
    logger.info("Готово")


app = FastAPI(title='CorpKnow AI', lifespan=lifespan)

app.include_router(router=auth_router)