import uuid
from dataclasses import dataclass
from db.base import db as database_config


@dataclass
class Price(database_config.Model):
    price: int
    coin: str
    timestamp: str

    id = database_config.Column(database_config.String(
    ), primary_key=True, default=lambda: str(uuid.uuid4()))
    price = database_config.Column(database_config.Integer())
    coin = database_config.Column(database_config.String())
    timestamp = database_config.Column(database_config.DateTime())
