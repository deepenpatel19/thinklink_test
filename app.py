import logging
import os
from api.prices import api

from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

from db.base import db as database_config
from tasks.price_task import check_btc_price
from tasks.mail_task import mail_initialization

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(
                        os.getpid()),
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.StreamHandler()])

logger = logging.getLogger()


def create_app():
    logger.info(f'Starting app in development environment')
    basedir = os.path.abspath(os.path.dirname(__file__))

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['MAIL_SERVER'] = os.environ.get("smtp_host")
    app.config['MAIL_PORT'] = int(os.environ.get("smtp_port"))
    app.config['MAIL_USERNAME'] = os.environ.get("smtp_username")
    app.config['MAIL_PASSWORD'] = os.environ.get("smtp_password")
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    api.init_app(app)
    mail_initialization(app)

    database_config.init_app(app)
    with app.app_context():
        database_config.create_all()

    scheduler = BackgroundScheduler(
        {'apscheduler.job_defaults.max_instances': 2})
    scheduler.start()
    scheduler.add_job(func=check_btc_price, trigger="interval",
                      seconds=30, kwargs={"app": app})

    atexit.register(lambda: scheduler.shutdown())

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
