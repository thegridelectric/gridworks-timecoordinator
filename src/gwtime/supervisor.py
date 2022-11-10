""" AtnActorBase """
import functools
import logging
import traceback
from typing import Any
from typing import Optional
from typing import no_type_check

import pendulum

from gwtime.actor_base import ActorBase
from gwtime.config import SupervisorSettings
from gwtime.enums import GNodeRole
from gwtime.enums import MessageCategorySymbol
from gwtime.enums import UniverseType
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
        super().__init__(settings=settings)  # type: ignore

        self.latest_time_unix_s: Optional[int] = None

    def additional_rabbit_stuff_after_rabbit_base_setup_is_done(self):
        rjb = MessageCategorySymbol.rjb.value
        tc_alias_lrh = self.settings.my_time_coordinator_alias.replace(".", "-")
        binding = f"{rjb}.{tc_alias_lrh}.timecoordinator.sim-timestep"

        cb = functools.partial(self.on_timecoordinator_bindok, binding=binding)
        self._consume_channel.queue_bind(
            self.queue_name, "timecoordinatormic_tx", routing_key=binding, callback=cb
        )

    @no_type_check
    def on_timecoordinator_bindok(self, _unused_frame, binding) -> None:
        LOGGER.info(f"Queue {self.queue_name} bound with {binding}")

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
