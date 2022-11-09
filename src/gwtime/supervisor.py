""" AtnActorBase """
import logging
import traceback
from abc import abstractmethod
from typing import Any
from typing import Optional

import pendulum

from gwtime.actor_base import ActorBase
from gwtime.config import SupervisorSettings
from gwtime.enums import GNodeRole
from gwtime.schemata import HeartbeatA
from gwtime.schemata import HeartbeatA_Maker


LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class Supervisor(ActorBase):
    def __init__(self, settings: SupervisorSettings):
        super().__init__(settings=settings) # type: ignore

        LOGGER.debug("debug")
        LOGGER.info("info")
        LOGGER.warning("warning")
        self.latest_time_unix_s: Optional[int] = None

    ########################
    # Sends
    ########################

    def prepare_for_death(self) -> None:
        self.actor_main_stopped = True

    ########################
    # Receives
    ########################

    def route_message(
        self, from_alias: str, from_role: GNodeRole, payload: HeartbeatA
    ) -> None:
        if payload.TypeName == HeartbeatA_Maker.type_name:
            try:
                self.heartbeat_a_received(from_alias, from_role, payload)
            except:
                LOGGER.warning("Error in g_node_ready_received")
                LOGGER.warning(traceback.format_exc(True))
        else:
            LOGGER.info(f"Does not process TypeName {payload.TypeName}")
            return

    def heartbeat_a_received(
        self, from_alias: str, from_role: GNodeRole, payload: HeartbeatA
    ) -> None:
        LOGGER.warning(
            f"Received heartbeat from {from_alias} of role {from_role.value}"
        )

    # @property
    # def latest_time_utc(self) -> Optional(pendulum.DateTime):
    #     if self.latest_time_unix_s is None:
    #         return None
    #     return pendulum.from_timestamp(self.latest_time_unix_s)
