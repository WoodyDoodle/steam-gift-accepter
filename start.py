import os
import time
import logging
import traceback
from datetime import datetime

from dotenv import load_dotenv
from steampy.client import SteamClient, TradeOfferState

from src.database import (AppID, SteamItem, 
                          init_db, get_db_session, 
                          get_cs2_item_from_dict)


logger = logging.getLogger('__name__')

load_dotenv()

API_KEY = os.environ.get('STEAM_API_KEY')
STEAMGUARD_PATH = os.environ.get('STEAMGUARD_PATH')
STEAM_USERNAME = os.environ.get('STEAM_USERNAME')
STEAM_PASSWORD = os.environ.get('STEAM_PASSWORD')
TIMEOUT = int(os.environ.get('TIME_OUT'))
DB_URL = os.environ.get('DATABASE_URL')

LOG_FILE_NAME = os.environ.get('LOG_FILE_NAME')
LOG_FILE_PATH = os.environ.get('LOG_FILE_PATH')

def main() -> None:
    if not are_credentials_filled():
        logger.error('Incorrectly specified environment variables')
        return

    logger.info('Initializing the database')
    try:
        init_db(DB_URL)
    except Exception as e:
        logger.error(f'Database initialization failed: {e}')
        traceback.print_exc()
        return

    db_session = get_db_session(DB_URL)

    client = SteamClient(API_KEY)
    try:
        client.login(STEAM_USERNAME, STEAM_PASSWORD, STEAMGUARD_PATH)
    except KeyError:
        logger.error('Error while logging in. You may need to wait...')
        logger.info('Waiting 60 sec...')
        time.sleep(60)
        client.login(STEAM_USERNAME, STEAM_PASSWORD, STEAMGUARD_PATH)

    logger.info(f'Successful authorization <<{STEAM_USERNAME}>> in Steam. Start of bot work')
    
    while True:
        offers = client.get_trade_offers(use_webtoken=True)['response']['trade_offers_received']
        for offer in offers:
            if is_donation(offer):
                offer_id = offer['tradeofferid']
                count_accepted_items = len(offer['items_to_receive'])
                client.accept_trade_offer(offer_id)
                for item in offer['items_to_receive']:
                    item_ = offer['items_to_receive'][item]
                    if int(item_['appid']) == AppID.CS2:
                        db_item = get_cs2_item_from_dict(item_)
                        db_session.add(db_item)
                        db_session.commit()
                logger.info(f'Accepted trade offer {offer_id}. Got {count_accepted_items} items')
        time.sleep(TIMEOUT)


def are_credentials_filled() -> bool:
    return all((API_KEY, STEAMGUARD_PATH, STEAM_USERNAME, STEAM_PASSWORD))


def is_donation(offer: dict) -> bool:
    return (
        offer.get('items_to_receive')
        and not offer.get('items_to_give')
        and offer['trade_offer_state'] == TradeOfferState.Active
        and not offer['is_our_offer']
    )


if __name__ == '__main__':
    log_file_path = os.path.join(LOG_FILE_PATH, f"{str(datetime.now().date()) + '_' + LOG_FILE_NAME}")
    logging.basicConfig(level=logging.INFO,
                        filename=log_file_path,
                        format='%(asctime)s - [%(levelname)s] - %(message)s')
    main()