import logging
import requests
import json
import os
from models.price import Price
from datetime import datetime
from db.base import db as database_config
from .mail_task import send_email

logger = logging.getLogger()


def check_btc_price(*args, **kwargs):
    logger.debug("check btc price")
    url = "https://api.coingecko.com/api/v3/coins/bitcoin?tickers=true&market_data=true&community_data=true&developer_data=true&sparkline=true"
    request = requests.get(url)
    if request.status_code == 200:
        response = json.loads(request.content)
        tickers = response.get("tickers", [])
        for index, value in enumerate(tickers):
            if value.get("base", "") == "BTC" and value.get("target", "") == "USD" and value.get("market", {}).get("identifier", "") == "currency":
                last_price = int(value.get("last"))
                price_object = Price(
                    coin="btc",
                    price=last_price,
                    timestamp=datetime.now()
                )
                logger.debug("price object {0}".format(price_object))
                app = kwargs.get("app")
                with app.app_context():
                    database_config.session.add(price_object)
                    database_config.session.commit()

                if int(os.environ.get("min")) > last_price or last_price > int(os.environ.get("max")):
                    logger.debug("will trigger email to {0}".format(
                        os.environ.get("email")))
                    with app.app_context():
                        send_email()
