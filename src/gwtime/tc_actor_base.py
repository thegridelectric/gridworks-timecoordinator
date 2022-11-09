""" AtnActorBase """
import logging
import traceback
from abc import abstractmethod
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


LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)

LOGGER.setLevel(logging.INFO)


class TcActorBase(ActorBase):
    def __init__(self, settings: Settings):
        super().__init__(settings=settings)
        self.latest_time_unix_s: Optional[int] = None

    ########################
    # Sends
    ########################

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
            to_g_node_alias="dw1.super1",
        )

    def prepare_for_death(self) -> None:
        self.actor_main_stopped = True

    ########################
    # Receives
    ########################

    def route_message(self, from_alias: str, from_role: GNodeRole, payload: HeartbeatA) -> None:
        if payload.TypeName == Ready_Maker.type_name:
            try:
                self.g_node_ready_received(payload)
            except:
                LOGGER.warning("Error in g_node_ready_received")
                LOGGER.warning(traceback.format_exc(True))
        else:
            LOGGER.info(f"Does not process TypeName {payload.TypeName}")
            return


    @abstractmethod
    def g_node_ready_received(self, payload: Ready) -> None:
        raise NotImplementedError

    # @property
    # def latest_time_utc(self) -> Optional(pendulum.DateTime):
    #     if self.latest_time_unix_s is None:
    #         return None
    #     return pendulum.from_timestamp(self.latest_time_unix_s)
