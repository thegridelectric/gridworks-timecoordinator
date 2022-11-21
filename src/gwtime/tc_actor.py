""" TimeCoordinator """
import logging
import threading
import time
import traceback
import uuid
from typing import List
from typing import Optional
from typing import no_type_check

import dotenv
import pendulum

import gwtime.config as config
from gwtime.actor_base import ActorBase
from gwtime.enums import GNodeRole
from gwtime.enums import MessageCategory
from gwtime.schemata import HeartbeatA
from gwtime.schemata import HeartbeatA_Maker
from gwtime.schemata import PauseTime
from gwtime.schemata import PauseTime_Maker
from gwtime.schemata import Ready
from gwtime.schemata import Ready_Maker
from gwtime.schemata import ResumeTime
from gwtime.schemata import ResumeTime_Maker
from gwtime.schemata import SimTimestep
from gwtime.schemata import SimTimestep_Maker


LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)

LOGGER.setLevel(logging.INFO)


class TcActor(ActorBase):
    def __init__(
        self,
        settings: config.Settings = config.Settings(_env_file=dotenv.find_dotenv()),
    ):
        super().__init__(settings=settings)
        self.timestep: SimTimestep = SimTimestep_Maker(
            from_g_node_alias=self.alias,
            from_g_node_instance_id=self.settings.g_node_instance_id,
            time_unix_s=self.settings.initial_time_unix_s,
            irl_time_unix_ms=int(time.time() * 1000),
            message_id=str(uuid.uuid4()),
        ).tuple

        self._time: int = self.settings.initial_time_unix_s
        self.my_actors: List[str] = [
            "d1.isone.ver.keene.holly",
            "d1.isone.ver.keene",
            # "dummy",
        ]
        self.ready: List[str] = []
        self.tickles: int = 0
        self.on_time: bool = True
        self.paused: bool = True
        self.tickle_thread: threading.Thread = threading.Thread(target=self.tickle_time)
        LOGGER.info(f"time initialized. waits for {self.my_actors}")

    ########################
    # Sends
    ########################

    def on_rabbit_ready(self) -> None:
        LOGGER.info("in on_rabbit_ready")
        self.tickle_thread.start()

    def resume(self) -> None:
        self.timestep.IrlTimeUnixMs = int(time.time() * 1000)
        self.tickles = 0
        self.paused = False
        self.send_time()

    def pause(self) -> None:
        self.paused = True

    def send_time(self) -> None:
        LOGGER.info(f"{self.time_utc_str()}")
        if self.paused:
            LOGGER.info(f"not sending time. Paused")
            return
        self.send_message(
            payload=self.timestep,
            message_category=MessageCategory.RabbitJsonBroadcast,
        )

    def tickle_time(self) -> None:
        LOGGER.info("Started tickle thread")
        base_sleep = 0.5
        ts = self._time
        while self.shutting_down is False:
            if self.paused:
                time.sleep(2)
            else:
                if self._time > ts:
                    ts = self._time
                    self.tickles = 0
                if self.on_time:
                    elapsed = time.time() - (self.timestep.IrlTimeUnixMs / 1000)
                    if elapsed > base_sleep:
                        self.on_time = False
                        self.tickles = 1
                        LOGGER.info(f"Tickle {self.tickles}")
                        self.send_time()
                    time.sleep(base_sleep)
                else:
                    self.tickles += 1
                    waiting_s = 2 ** (self.tickles - 1)
                    time.sleep(waiting_s)
                    elapsed = time.time() - (self.timestep.IrlTimeUnixMs / 1000)
                    missing = list(set(self.my_actors) - set(self.ready))
                    LOGGER.info(f"Tickle {self.tickles}, missing {missing}")

                    self.send_time()
                    if self.tickles >= 5:
                        self.paused = True
                        LOGGER.info(f"Pausing time after 5 tickles")

    @no_type_check
    def send_heartbeat_to_super(self) -> None:
        self.send_message(
            payload=HeartbeatA_Maker().tuple,
            to_role=GNodeRole.Supervisor,
            to_g_node_alias=self.settings.my_super_alias,
        )

    def prepare_for_death(self) -> None:
        self.tickle_thread.join()
        self.actor_main_stopped = True

    ########################
    # Receives
    ########################

    def route_message(
        self, from_alias: str, from_role: GNodeRole, payload: HeartbeatA
    ) -> None:
        if payload.TypeName == Ready_Maker.type_name:
            try:
                self.ready_received(payload)
            except:
                LOGGER.warning("Error in g_node_ready_received")
                LOGGER.warning(traceback.format_exc(True))
        elif payload.TypeName == PauseTime_Maker.type_name:
            try:
                self.pause_time_received(payload)
            except:
                LOGGER.warning("Error in pause_time_received")
                LOGGER.warning(traceback.format_exc(True))
        elif payload.TypeName == ResumeTime_Maker.type_name:
            try:
                self.resume_time_received(payload)
            except:
                LOGGER.warning("Error in resume_time_received")
                LOGGER.warning(traceback.format_exc(True))
        else:
            LOGGER.info(f"Does not process TypeName {payload.TypeName}")
            return

    def step(self, reset: bool = False) -> None:
        if reset == True:
            self._time = self.settings.initial_time_unix_s
        else:
            self._time += self.settings.time_step_duration_s
        self.timestep = SimTimestep_Maker(
            from_g_node_alias=self.alias,
            from_g_node_instance_id=self.settings.g_node_instance_id,
            time_unix_s=self._time,
            irl_time_unix_ms=int(time.time() * 1000),
            message_id=str(uuid.uuid4()),
        ).tuple
        self.on_time = True
        self.ready = []

    def ready_received(self, payload: Ready) -> None:
        if payload.FromGNodeAlias in self.my_actors:
            if payload.FromGNodeAlias not in self.ready:
                self.ready.append(payload.FromGNodeAlias)
            if set(self.ready) == set(self.my_actors):
                elapsed = time.time() - (self.timestep.IrlTimeUnixMs / 1000)
                LOGGER.info(f"Timestep took {round(elapsed,2)}s")
                self.step()
                self.send_time()

    def pause_time_received(self, payload: PauseTime):
        LOGGER.info(f"Received Pause message")
        self.pause()

    def resume_time_received(self, payload: ResumeTime):
        LOGGER.info(f"Received Resume message")
        self.resume()

    def time_utc_str(self) -> str:
        return pendulum.from_timestamp(self._time).strftime("%m/%d/%Y, %H:%M")
