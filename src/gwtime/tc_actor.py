""" AtnActorBase """
import logging
import time
import traceback
import uuid
from typing import Optional
from typing import no_type_check

import pendulum

from gwtime.actor_base import ActorBase
from gwtime.config import Settings
from gwtime.enums import GNodeRole
from gwtime.enums import MessageCategory
from gwtime.schemata import HeartbeatA
from gwtime.schemata import HeartbeatA_Maker
from gwtime.schemata import Ready
from gwtime.schemata import Ready_Maker
from gwtime.schemata import SimTimestep
from gwtime.schemata import SimTimestep_Maker


LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)

LOGGER.setLevel(logging.INFO)


class TcActor(ActorBase):
    def __init__(self, settings: Settings):
        super().__init__(settings=settings)
        self.latest_time_unix_s: Optional[int] = None

    ########################
    # Sends
    ########################

    def on_rabbit_ready(self):
        LOGGER.info("in on_rabbit_ready")
        d = pendulum.datetime(year=2020, month=1, day=1, hour=0)
        t = d.int_timestamp
        payload = SimTimestep_Maker(
            from_g_node_alias=self.alias,
            from_g_node_instance_id=self.settings.g_node_instance_id,
            time_unix_s=t,
            irl_time_unix_s=int(time.time()),
            message_id=str(uuid.uuid4()),
        ).tuple
        LOGGER.info(f"About to send first timestep {payload}")
        self.send_timestep(payload)

    def send_timestep(self, payload: SimTimestep) -> None:
        if type(payload) != SimTimestep:
            LOGGER.info(f"NOT SENDING. payload must be HackState, got {type(payload)} ")
            return None
        self.send_message(
            payload=payload, message_category=MessageCategory.RabbitJsonBroadcast
        )

    @no_type_check
    def send_heartbeat_to_super(self) -> None:
        self.send_message(
            payload=HeartbeatA_Maker().tuple,
            to_role=GNodeRole.Supervisor,
            to_g_node_alias=self.settings.my_super_alias,
        )

    def prepare_for_death(self) -> None:
        self.actor_main_stopped = True

    ########################
    # Receives
    ########################

    def route_message(
        self, from_alias: str, from_role: GNodeRole, payload: HeartbeatA
    ) -> None:
        if payload.TypeName == Ready_Maker.type_name:
            try:
                self.g_node_ready_received(payload)
            except:
                LOGGER.warning("Error in g_node_ready_received")
                LOGGER.warning(traceback.format_exc(True))
        else:
            LOGGER.info(f"Does not process TypeName {payload.TypeName}")
            return

    # @abstractmethod
    def g_node_ready_received(self, payload: Ready) -> None:
        LOGGER.info("Received ready from actor")
        raise NotImplementedError

    # @property
    # def latest_time_utc(self) -> Optional(pendulum.DateTime):
    #     if self.latest_time_unix_s is None:
    #         return None
    #     return pendulum.from_timestamp(self.latest_time_unix_s)
