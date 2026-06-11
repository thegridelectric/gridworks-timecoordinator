"""Hello-world time coordinator: broadcast sim.timestep on the broker.

Run it with::

    uv run tc-hello --beat-seconds 5 --step-seconds 60

Against the broker at ``GWBASE_RABBIT__URL`` (default: a local dev rabbit
at ``amqp://smqPublic:smqPublic@localhost:5672/d1__1``). Every
``--beat-seconds`` of wall time the coordinator broadcasts a
``sim.timestep`` advancing simulated time by ``--step-seconds`` — so sim
time can already run faster than wall time. Free-running hello mode: no
Ready barrier yet.
"""

import argparse
import logging
import time
import uuid

import pika
from gwbase import topology
from gwbase.config import ServiceSettings
from gwbase.orchestrator import Orchestrator
from gwbase.sema.types import SimTimestep
from gwbase.transport_encoding import RoutingEnvelope, TransportClass

LOGGER = logging.getLogger(__name__)

DEFAULT_ALIAS = "d1.tc"
DEFAULT_BEAT_SECONDS = 10.0
DEFAULT_STEP_SECONDS = 60


def provision_topology(url: str) -> None:
    """Declare the shared exchange fabric (idempotent) before the actor
    starts — actors only passively assert their consume exchange exists."""
    conn = pika.BlockingConnection(pika.URLParameters(url))
    try:
        ch = conn.channel()
        for ex in topology.exchanges():
            ch.exchange_declare(
                exchange=ex.name,
                exchange_type=ex.exchange_type,
                durable=ex.durable,
                internal=ex.internal,
            )
        for b in topology.exchange_bindings():
            ch.exchange_bind(
                destination=b.destination,
                source=b.source,
                routing_key=b.routing_key,
            )
    finally:
        conn.close()


class HelloTimeCoordinator(Orchestrator):
    """The smallest time coordinator. Not a GNode: plain ServiceSettings
    identity, alias in the GNode tree (d1.tc), TimeCoordinator transport
    class. Broadcasts sim.timestep; Ready answers from participants land
    in process_message and are logged, nothing more — the barrier comes
    later."""

    def __init__(self, *, settings: ServiceSettings, my_super_alias: str = "d1.super1"):
        super().__init__(
            settings=settings,
            transport_class=TransportClass.TimeCoordinator,
            my_super_alias=my_super_alias,
            # A root coordinator answers to no other clock; name ourselves.
            my_time_coordinator_alias=settings.service_alias,
        )

    def process_message(self, *, envelope: RoutingEnvelope, body: bytes) -> None:
        LOGGER.info(
            "[%s] received %s from %s",
            self.alias,
            envelope.type_name,
            envelope.from_alias,
        )

    def broadcast_timestep(self, time_unix_s: int) -> None:
        ts = SimTimestep(
            from_g_node_alias=self.alias,
            from_g_node_instance_id=self.instance_id,
            time_unix_s=time_unix_s,
            timestep_created_ms=int(time.time() * 1000),
            message_id=str(uuid.uuid4()),
        )
        self.send(
            envelope=self.broadcast_envelope(type_name=ts.type_name),
            body=ts.to_bytes(),
        )
        LOGGER.info("[%s] sim time -> %s", self.alias, time_unix_s)


def wait_for_consuming(actor: Orchestrator, timeout_s: float = 10.0) -> None:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if actor._consuming:  # noqa: SLF001
            return
        time.sleep(0.05)
    raise RuntimeError(f"{actor.alias} did not start consuming within {timeout_s}s")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--beat-seconds",
        type=float,
        default=DEFAULT_BEAT_SECONDS,
        help=f"wall-clock broadcast cadence (default {DEFAULT_BEAT_SECONDS})",
    )
    parser.add_argument(
        "--step-seconds",
        type=int,
        default=DEFAULT_STEP_SECONDS,
        help=f"simulated seconds advanced per beat (default {DEFAULT_STEP_SECONDS})",
    )
    parser.add_argument(
        "--start-unix-s",
        type=int,
        default=None,
        help="simulated start time (default: now)",
    )
    parser.add_argument(
        "--no-provision",
        action="store_true",
        help="skip declaring the exchange topology (it already exists)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logging.getLogger("pika").setLevel(logging.WARNING)

    settings = ServiceSettings(
        service_alias=DEFAULT_ALIAS, service_name="timecoordinator"
    )
    if not args.no_provision:
        provision_topology(settings.rabbit.url.get_secret_value())

    tc = HelloTimeCoordinator(settings=settings)
    tc.start()
    sim_time = args.start_unix_s if args.start_unix_s is not None else int(time.time())
    try:
        wait_for_consuming(tc)
        LOGGER.info(
            "[%s] consuming; beating every %.1fs, advancing %ss per beat",
            tc.alias,
            args.beat_seconds,
            args.step_seconds,
        )
        while True:
            tc.broadcast_timestep(sim_time)
            time.sleep(args.beat_seconds)
            sim_time += args.step_seconds
    except KeyboardInterrupt:
        LOGGER.info("[%s] interrupted; stopping", tc.alias)
    finally:
        tc.stop()


if __name__ == "__main__":
    main()
