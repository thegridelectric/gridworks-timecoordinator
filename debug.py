import time

import pendulum

from gwtime.config import Settings
from gwtime.tc_actor import TcActor


settings = Settings()
tc = TcActor(settings=Settings())
tc.start()


tc.resume()
tc.pause()
