from fastapi import APIRouter, Depends, HTTPException
from app.token.token import get_current_user
from app.services.rapidapi import get_fund_houses, get_open_ended_schemes
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/houses")
async def fetch_fund_houses(current_user: str = Depends(get_current_user)):
    try:
        result = await get_fund_houses()
        logger.info("Fetched fund houses successfully")
        return result
    except Exception as e:
        logger.error(f"Error fetching fund houses: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to fetch fund houses: {str(e)}")

@router.get("/schemes")
async def fetch_open_schemes(fund_family: str, current_user: str = Depends(get_current_user)):
    try:
        result = await get_open_ended_schemes(fund_family)
        logger.info(f"Fetched open-ended schemes for fund family: {fund_family}")
        return result
    except Exception as e:
        logger.error(f"Error fetching schemes for fund family '{fund_family}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to fetch open-ended schemes: {str(e)}")