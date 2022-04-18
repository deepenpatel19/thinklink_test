from flask import jsonify, request, abort
from flask_restful import Api, Resource
from models.price import Price
from models.crud.crud_price import PriceCrudOperation
from datetime import datetime
import logging
api = Api(prefix="/api")

logger = logging.getLogger()


class BitcoinPrice(Resource):

    def get(self):
        args = request.args
        date = args.get("date", "")
        offset = args.get("offset", "1")  # Set 1 as default
        limit = args.get("limit", "10")  # Set 10 as default
        url = "http://127.0.0.1:5000/prices/btc"
        # logger.debug("date {0}".format(date))
        if date:
            try:
                date = datetime.strptime(date, "%d-%m-%Y")
            except Exception as e:
                date = ""
        # logger.debug("date object {0}".format(date))

        results = PriceCrudOperation.get_query(date=date)
        # logger.debug("results {0}".format(results))

        try:
            offset = int(offset)
        except ValueError as e:
            offset = 1

        try:
            limit = int(limit)
        except ValueError as e:
            limit = 10

        offset = int(offset)
        limit = int(limit)
        count = len(results)
        obj = {}
        obj['count'] = count

        query_params_dict = {
            "next_url": True
        }
        if offset + limit > count:
            query_params_dict["next_url"] = False
        else:
            offset_copy = offset + limit
            query_params_dict["next_offset"] = offset_copy
            query_params_dict["next_limit"] = limit

        current_url = url
        next_url = url
        if date:
            current_url = current_url + "?date={0}".format(date)
            next_url = next_url + "?date={0}".format(date)

        if limit and "?" in current_url:
            current_url = current_url + "&limit={0}".format(limit)
        elif limit:
            current_url = current_url + "?limit={0}".format(limit)

        if offset and "?" in current_url:
            current_url = current_url + "&offset={0}".format(offset)
        elif offset:
            current_url = current_url + "?offset={0}".format(offset)

        obj["url"] = current_url

        if query_params_dict.get("next_url"):

            if query_params_dict.get("next_limit") and "?" in next_url:
                next_url = next_url + \
                    "&limit={0}".format(query_params_dict.get("next_limit"))
            elif query_params_dict.get("next_limit"):
                next_url = next_url + \
                    "?limit={0}".format(query_params_dict.get("next_limit"))

            if query_params_dict.get("next_offset") and "?" in next_url:
                next_url = next_url + \
                    "&offset={0}".format(query_params_dict.get("next_offset"))
            elif query_params_dict.get("next_offset"):
                next_url = url + \
                    "?offset={0}".format(query_params_dict.get("next_offset"))
        else:
            next_url = ""

        obj["next"] = next_url

        obj['data'] = results[(offset - 1):(offset - 1 + limit)]
        return jsonify(obj)


api.add_resource(BitcoinPrice, '/prices/btc')
