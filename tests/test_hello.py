import json
import time

import pika
import pytest
from gwbase.config import ServiceSettings

from gwtc.hello import HelloTimeCoordinator, provision_topology, wait_for_consuming


@pytest.fixture
def settings() -> ServiceSettings:
    return ServiceSettings(service_alias="d1.tc")


def test_hello_constructs_without_broker(settings):
    tc = HelloTimeCoordinator(settings=settings)
    assert tc.alias == "d1.tc"
    assert tc.routing_code == "time"
    assert tc._consume_exchange == "time_tx"  # noqa: SLF001
    assert tc._publish_exchange == "timemic_tx"  # noqa: SLF001


@pytest.mark.live
def test_timesteps_are_seen_heard(settings):
    """The terminalasset hello-world lesson: an observer queue on
    timemic_tx must actually RECEIVE consecutive timesteps with
    advancing TimeUnixS — sent is not enough."""
    url = settings.rabbit.url.get_secret_value()
    provision_topology(url)

    # Observer binds BEFORE the coordinator beats — what a real child does.
    conn = pika.BlockingConnection(pika.URLParameters(url))
    ch = conn.channel()
    q = ch.queue_declare(queue="", exclusive=True).method.queue
    ch.queue_bind(queue=q, exchange="timemic_tx", routing_key="#")

    tc = HelloTimeCoordinator(settings=settings)
    tc.start()
    try:
        wait_for_consuming(tc)
        start = 1_700_000_000
        tc.broadcast_timestep(start)
        tc.broadcast_timestep(start + 60)

        seen = []
        deadline = time.time() + 5
        while len(seen) < 2 and time.time() < deadline:
            method, _props, body = ch.basic_get(queue=q, auto_ack=True)
            if method is None:
                time.sleep(0.05)
                continue
            payload = json.loads(body)
            if payload.get("TypeName") == "sim.timestep":
                seen.append(payload["TimeUnixS"])
        assert seen == [start, start + 60]
    finally:
        tc.stop()
        conn.close()
