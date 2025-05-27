import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker


load_dotenv()
TABLE_NAME = os.environ.get('TABLE_NAME')
DATABASE_URL = os.environ.get('DATABASE_URL')

Base = declarative_base()

class AppID:
    CS2 = 730

class SteamItem(Base):
    __tablename__ = TABLE_NAME

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer)
    classid = Column(Integer)
    instanceid = Column(Integer)
    amount = Column(Integer)
    market_hash_name = Column(String)

def init_db(db_url = DATABASE_URL):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False)
    return engine, Session

def get_db_session(db_url=DATABASE_URL):
    _, Session = init_db(db_url)
    return Session()

def get_cs2_item_from_dict(item: dict) -> SteamItem:
    if item['appid'] != AppID.CS2:
        return None
    
    return SteamItem(
        item_id=int(item['id']),
        classid=item['classid'],
        instanceid=item['instanceid'],
        amount=item['amount'],
        market_hash_name=item['market_hash_name']
    )
