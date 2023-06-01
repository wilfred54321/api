import logging
from api.config import Config
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s in %(module)s at %(asctime)s ::: %(message)s')

file_handler = logging.FileHandler(Config.MAIN_LOGS)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
