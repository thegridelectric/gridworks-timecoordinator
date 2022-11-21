import logging
import time

import dotenv

from gwtime.config import Settings
from gwtime.tc_actor import TcActor


settings = Settings()
tc = TcActor(settings=Settings(_env_file=dotenv.find_dotenv()))
time.sleep(30)

tc.start()
