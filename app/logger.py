import logging

# from pythonjsonlogger import jsonlogger

logger = logging.getLogger("worker")

logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
# formatter = jsonlogger.JsonFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# handler.setFormatter(formatter)
logger.addHandler(handler)
