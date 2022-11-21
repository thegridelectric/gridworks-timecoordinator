import logging

import dotenv

from gwtime.config import Settings
from gwtime.tc_actor import TcActor


settings = Settings()
tc = TcActor(settings=Settings(_env_file=dotenv.find_dotenv()))
tc.start()
