import logging
import sys
from nicelog.formatters import Colorful

logger = logging.getLogger('exp1rms')
logger.setLevel(logging.INFO)

# Setup a handler, writing colorful output to the console
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(Colorful())
handler.setLevel(logging.INFO)
logger.addHandler(handler)
