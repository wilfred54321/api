import logging
from api.config import Config
# logging.basicConfig(level=logging.INFO,filename="api.log",
#                     format = '%(asctime)s] %(levelname)s in %(module)s: %(message)s')
#
# logging configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s] %(levelname)s in %(module)s: %(message)s')

file_handler = logging.FileHandler(Config.API_ADMIN_LOGS)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
