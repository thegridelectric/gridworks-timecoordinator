import logging
import time


screen_handler = logging.StreamHandler()
fmt = "%(asctime)s  %(filename)s  %(message)s"
screen_handler.setFormatter(logging.Formatter(fmt=fmt))
logging.getLogger().addHandler(screen_handler)


from gwtime.config import Settings
from gwtime.tc_actor import TcActor


tc = TcActor(settings=Settings())
tc.start()

time.sleep(5)
tc.stop()
