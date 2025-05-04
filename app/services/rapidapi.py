import logging
from app.config import rapidapi_key, rapidapi_host, rapidapi_url
from app.db import SessionLocal
from models import NAV
from datetime import datetime
from pytz import UTC
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

headers = {
    "X-RapidAPI-Key": rapidapi_key,
    "X-RapidAPI-Host": rapidapi_host
}

async def get_fund_houses():
    querystring = {"Scheme_Type": "Open"}
    try:
        response = requests.get(rapidapi_url, headers=headers, params=querystring)
        data = response.json()
        unique_families = list({entry['Mutual_Fund_Family'] for entry in data})
        return unique_families
    except requests.RequestException as e:
        logger.error(f"Failed to fetch fund houses: {e}")
        return []
    except Exception as e:
        logger.exception(f"Unexpected error in get_fund_houses: {str(e)}")
        return []


async def get_open_ended_schemes(fund_family):
    querystring = {"Scheme_Type": "Open", "Mutual_Fund_Family": fund_family}
    try:
        response = requests.get(rapidapi_url, headers=headers, params=querystring)
        data = response.json()
        open_ended_schemes = [{entry["Scheme_Code"], entry["Scheme_Name"]} for entry in data]
        return open_ended_schemes
    except requests.RequestException as e:
        logger.error(f"Failed to fetch schemes for {fund_family}: {e}")
        return []
    except Exception as e:
        logger.exception(f"Unexpected error in get_open_ended_schemes: {str(e)}")
        return []

def update_all_navs():
    db = SessionLocal()
    try:
        scheme_codes = db.query(NAV.scheme_code).all()
        for code, in scheme_codes:
            querystring = {"Scheme_Code": int(code)}

            headers = {
                "x-rapidapi-key": rapidapi_key,
                "x-rapidapi-host": rapidapi_host
            }

            try:
                response = requests.get(rapidapi_url, headers=headers, params=querystring)
                if response.status_code == 200:
                    data = response.json()
                    nav_value = float(data[0].get("Net_Asset_Value", 0))
                    db_nav = db.query(NAV).filter(NAV.scheme_code == code).first()
                    if db_nav:
                        db_nav.nav = nav_value
                        db_nav.last_updated = datetime.now(UTC)
                    else:
                        db_nav = NAV(scheme_code=code, nav=nav_value, last_updated=datetime.now(UTC))
                        db.add(db_nav)
            except (requests.RequestException, ValueError, KeyError) as e:
                logger.error(f"Error updating NAV for Scheme_Code {code}: {e}")
        db.commit()
    except Exception as e:
        logger.exception(f"Unexpected error during NAV update: {str(e)}")
    finally:
        db.close()