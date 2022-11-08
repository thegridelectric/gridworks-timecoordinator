""" AtnActorBase """
import logging
import traceback
from abc import abstractmethod
from typing import Optional

import pendulum

from gwtime.actor_base import ActorBase
from gwtime.config import Settings
from gwtime.enums import GNodeRole
from gwtime.schemata import HeartbeatA
from gwtime.schemata import Ready
from gwtime.schemata import Ready_Maker
from gwtime.schemata import SimTimestep


LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)

LOGGER.setLevel(logging.INFO)

import enum


class RoutingKeyType(enum.Enum):
    JSON_DIRECT_MESSAGE = "rj"
    JSON_BROADCAST = "rjb"
    GW_MQTT = "mq"
    GW_SERIAL = "s"


class AtnActorBase(ActorBase):
    def __init__(self, settings: Settings):
        super().__init__(settings=settings)
        self.latest_time_unix_s: Optional[int] = None

    ########################
    ## Sends
    ########################

    def send_timestep(self, payload: SimTimestep) -> None:
        if type(payload) != SimTimestep:
            LOGGER.info(f"NOT SENDING. payload must be HackState, got {type(payload)} ")
            return None
        self.send_message(
            payload=payload,
            routing_key_type=RoutingKeyType.JSON_BROADCAST,
            radio_channel="time",
        )

    def prepare_for_death(self) -> None:
        self.actor_main_stopped = True

    ########################
    ## Receives
    ########################

    def route_message(self, from_role: GNodeRole, payload: HeartbeatA) -> None:
        match payload.TypeName:
            case Ready_Maker.type_name:
                if from_role == GNodeRole.MarketMaker:
                    try:
                        self.g_node_ready_received(payload)
                    except:
                        LOGGER.warning("Error in g_node_ready_received")
                        LOGGER.warning(traceback.format_exc(True))

    @abstractmethod
    def g_node_ready_received(self, payload: Ready) -> None:
        raise NotImplementedError

    @property
    def latest_time_utc(self) -> Optional(pendulum.DateTime):
        if self.latest_time_unix_s is None:
            return None
        return pendulum.from_timestamp(self.latest_time_unix_s)
