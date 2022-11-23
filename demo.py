import logging
import time

import dotenv
import pendulum


end = pendulum.datetime(year=2020, month=1, day=3, hour=5)

from gwtime.config import Settings
from gwtime.tc_actor import TcActor


tc = TcActor(settings=Settings(_env_file=dotenv.find_dotenv()))
time.sleep(30)


tc.start()

while tc._time < end.timestamp():
    time.sleep(2)

tc.stop()
