import logging
from ..price import Price

logger = logging.getLogger()


class PriceCrudOperation:

    @classmethod
    def get_query(cls, date=None):
        logger.debug("CRUD operation on Price table {0}".format(date))
        if date:
            return Price.query.filter(Price.timestamp >= date).all()
        else:
            return Price.query.all()
