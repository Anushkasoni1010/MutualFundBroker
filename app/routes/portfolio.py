from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import UserPortfolio, NAV
from app.token.token import get_current_user
from app.services.rapidapi import update_all_navs
from app.db import get_db
from fastapi.security import OAuth2PasswordBearer
from pytz import UTC
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

@router.post("/add")
def add_investment(fund_house: str, scheme_code: str, units: float, db: Session = Depends(get_db),
                   current_user: str = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    try:
        inv = UserPortfolio(user_id=current_user, fund_house=fund_house, scheme_code=scheme_code, units=units,
                            purchase_date=datetime.now(UTC))
        db.add(inv)
        nav_update = NAV(scheme_code=scheme_code, nav=0, last_updated=datetime.now(UTC))
        db.add(nav_update)
        db.commit()
        return {"msg": "Investment added"}
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error while adding investment for user {current_user}: {e}")
        raise HTTPException(status_code=500, detail="Failed to add investment")
    except Exception as e:
        db.rollback()
        logger.exception("Unexpected error in add_investment")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/")
def get_portfolio(db: Session = Depends(get_db), current_user: str = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    try:
        update_all_navs()
    except Exception as e:
        logger.warning(f"NAV update failed for user {current_user}: {e}")

    try:
        investments = db.query(UserPortfolio).filter(UserPortfolio.user_id == current_user).all()
        portfolio = []
        for inv in investments:
            nav = db.query(NAV).filter(NAV.scheme_code == inv.scheme_code).first()
            value = inv.units * nav.nav if nav else 0
            portfolio.append({"scheme_code": inv.scheme_code, "units": inv.units, "current_value": value})
        return portfolio
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching portfolio for user {current_user}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch portfolio")

    except Exception as e:
        logger.exception("Unexpected error in get_portfolio")
        raise HTTPException(status_code=500, detail="Internal server error")