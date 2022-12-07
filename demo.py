import logging
import time

import dotenv
import pendulum

from gwtime.config import Settings
from gwtime.tc_actor import TcActor


tc = TcActor(settings=Settings(_env_file=dotenv.find_dotenv()))
time.sleep(5)


tc.start()
