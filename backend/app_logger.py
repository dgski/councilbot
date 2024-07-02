import logging

import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(levelname)s: %(filename)s:%(lineno)d: %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S')
logger = logging