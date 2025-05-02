from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.services.rapidapi import get_fund_houses, get_open_ended_schemes
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

@router.get("/houses")
async def fetch_fund_houses(token: str = Depends(oauth2_scheme)):
    try:
        result = await get_fund_houses()
        logger.info("Fetched fund houses successfully")
        return result
    except Exception as e:
        logger.error(f"Error fetching fund houses: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch fund houses")

@router.get("/schemes")
async def fetch_open_schemes(fund_family: str, token: str = Depends(oauth2_scheme)):
    try:
        result = await get_open_ended_schemes(fund_family)
        logger.info(f"Fetched open-ended schemes for fund family: {fund_family}")
        return result
    except Exception as e:
        logger.error(f"Error fetching schemes for fund family '{fund_family}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch open-ended schemes")