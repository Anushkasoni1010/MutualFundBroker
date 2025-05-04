from fastapi import FastAPI
from app.routes import auth, funds, portfolio
from app.services.rapidapi import update_all_navs
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Mutual Fund API",
    description="A FastAPI project with JWT Auth and Mutual Fund Portfolio tracking",
    version="1.0.0",
    docs_url="/",  # Serve Swagger UI at root
    redoc_url=None
)

try:
    app.include_router(auth.router, prefix="/auth")
    app.include_router(funds.router, prefix="/funds")
    app.include_router(portfolio.router, prefix="/portfolio")
    logger.info("Routers registered successfully.")
except Exception as e:
    logger.exception(f"Failed to include one or more routers: {e}")
    sys.exit(1)

try:
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_all_navs, 'interval', hours=1)
    scheduler.start()
    logger.info("Scheduler started successfully.")
except Exception as e:
    logger.exception(f"Failed to start scheduler: {str(e)}")
    sys.exit(1)

