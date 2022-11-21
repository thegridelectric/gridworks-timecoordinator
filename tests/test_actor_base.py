# import json
# import os
# import time
# import uuid

# import pika

# from gnf.actor_base import RoutingKeyType
import gwtime.config as config
from gwtime.actor_base import OnReceiveMessageDiagnostic
from gwtime.actor_base import OnSendMessageDiagnostic
from gwtime.enums import MessageCategory
from gwtime.enums import MessageCategorySymbol
from gwtime.schemata import HeartbeatA
from gwtime.schemata import HeartbeatA_Maker

from .utils import SupervisorStubRecorder
from .utils import TimeCoordinatorStubRecorder
from .utils import wait_for


def test_actor_base():
    supervisor = SupervisorStubRecorder(settings=config.SupervisorSettings())
    tc = TimeCoordinatorStubRecorder(settings=config.Settings())
    result = tc.send_heartbeat_to_super()
    assert result == OnSendMessageDiagnostic.STOPPED_SO_NOT_SENDING

    supervisor.start()
    tc.start()

    wait_for(
        lambda: supervisor._consume_connection, 2, "actor._consume_connection exists"
    )
    wait_for(lambda: supervisor._consuming, 2, "actor is consuming")
    wait_for(
        lambda: supervisor._publish_connection.is_open,
        2,
        "actor publish connection is open",
    )

    assert supervisor.messages_received == 0
    assert supervisor.messages_routed_internally == 0

    send_diagnostic = tc.send_heartbeat_to_super()
    assert send_diagnostic == OnSendMessageDiagnostic.MESSAGE_SENT
    wait_for(
        lambda: supervisor.messages_received == 1,
        2,
        f"supervisor.messages_received is {supervisor.messages_received}",
    )
    assert supervisor.routing_to_super__heartbeat_a__worked == True

    supervisor.stop()
    tc.stop()


#     ####################################
#     # Testing actor_base.on_message
#     ###################################
#     supervisor._consume_channel.queue_bind(
#         supervisor.queue_name,
#         "gnrmic_tx",
#         routing_key="garbage.#",
#     )
#     supervisor._consume_channel.queue_bind(
#         supervisor.queue_name,
#         "gnrmic_tx",
#         routing_key="pubsub.#",
#     )
#     supervisor._consume_channel.queue_bind(
#         supervisor.queue_name,
#         "gnrmic_tx",
#         routing_key="json",
#     )
#     supervisor._consume_channel.queue_bind(
#         supervisor.queue_name,
#         "gnrmic_tx",
#         routing_key="json.*.crap.*.*",
#     )
#     time.sleep(0.5)

#     payload = HeartbeatA_Maker().tuple

#     properties = pika.BasicProperties(
#         reply_to=tc.queue_name,
#         app_id=tc.alias,
#         correlation_id=str(uuid.uuid4()),
#     )
#     tc._publish_channel.basic_publish(
#         exchange=tc._publish_exchange,
#         routing_key="unknown-message-category.d1-time",
#         body=payload.as_type(),
#         properties=properties,
#     )

#     wait_for(
#         lambda: supervisor.messages_received == 1, 2, f"gnf.messages_received is {supervisor.messages_received}"
#     )
#     assert supervisor.messages_received == 1
#     assert supervisor.messages_routed_internally == 0
#     assert (
#         supervisor._latest_on_message_diagnostic == OnReceiveMessageDiagnostic.TYPE_NAME_DECODING_PROBLEM
#     )

#     properties = pika.BasicProperties(
#         reply_to=tc.queue_name,
#         app_id=tc.alias,
#         type=MessageCategorySymbol.post,
#         correlation_id=str(uuid.uuid4()),
#     )

#     tc._publish_channel.basic_publish(
#         exchange=tc._publish_exchange,
#         routing_key="post.dwgps-gnr.the_latest_scoop_everybody_wants",
#         body=payload.as_type(),
#         properties=properties,
#     )
#     wait_for(
#         lambda: supervisor.messages_received == 2, 2, f"gnf.messages_received is {supervisor.messages_received}"
#     )
#     assert supervisor.messages_received == 2
#     assert supervisor.messages_routed_internally == 0
#     assert (
#         supervisor._latest_on_message_diagnostic == OnReceiveMessageDiagnostic.UNHANDLED_ROUTING_KEY_TYPE
#     )

#     properties = pika.BasicProperties(
#         reply_to=tc.queue_name,
#         app_id=tc.alias,
#         type=RoutingKeyType.JSON_DIRECT_MESSAGE.value,
#         correlation_id=str(uuid.uuid4()),
#     )
#     tc._publish_channel.basic_publish(
#         exchange=tc._publish_exchange,
#         routing_key="json.dwgps_gnr.gnr.gnf.dwgps_gnf",
#         body=json.dumps({"TypeName": "not.lrd.format_bro"}),
#         properties=properties,
#     )
#     wait_for(
#         lambda: supervisor.messages_received == 3, 2, f"gnf.messages_received is {supervisor.messages_received}"
#     )
#     assert supervisor.messages_received == 3
#     assert supervisor.messages_routed_internally == 0
#     assert (
#         supervisor._latest_on_message_diagnostic == OnReceiveMessageDiagnostic.TYPE_NAME_DECODING_PROBLEM
#     )

#     properties = pika.BasicProperties(
#         reply_to=tc.queue_name,
#         app_id=tc.alias,
#         type=RoutingKeyType.JSON_DIRECT_MESSAGE.value,
#         correlation_id=str(uuid.uuid4()),
#     )
#     tc._publish_channel.basic_publish(
#         exchange=tc._publish_exchange,
#         routing_key="json.dwgps_gnr.gnr.gnf.dwgps_gnf",
#         body=json.dumps({"TypeName": "esoteric.type.alias.100"}),
#         properties=properties,
#     )
#     wait_for(
#         lambda: supervisor.messages_received == 4, 2, f"gnf.messages_received is {supervisor.messages_received}"
#     )
#     assert supervisor.messages_received == 4
#     assert supervisor.messages_routed_internally == 0
#     assert supervisor._latest_on_message_diagnostic == OnReceiveMessageDiagnostic.UNKNOWN_type_name

#     tc._publish_channel.basic_publish(
#         exchange=tc._publish_exchange,
#         routing_key="json",
#         body=payload.as_type(),
#         properties=properties,
#     )
#     wait_for(
#         lambda: supervisor.messages_received == 5, 2, f"gnf.messages_received is {supervisor.messages_received}"
#     )
#     assert supervisor.messages_received == 5
#     assert supervisor.messages_routed_internally == 0
#     assert (
#         supervisor._latest_on_message_diagnostic == OnReceiveMessageDiagnostic.FROM_GNODE_DECODING_PROBLEM
#     )

#     tc._publish_channel.basic_publish(
#         exchange=tc._publish_exchange,
#         routing_key="json.bad-from_g_node_alias.gnr.gnf.dwgps_gnf",
#         body=payload.as_type(),
#         properties=properties,
#     )
#     wait_for(
#         lambda: supervisor.messages_received == 6, 2, f"gnf.messages_received is {supervisor.messages_received}"
#     )
#     assert supervisor.messages_received == 6
#     assert supervisor.messages_routed_internally == 0
#     assert (
#         supervisor._latest_on_message_diagnostic == OnReceiveMessageDiagnostic.FROM_GNODE_DECODING_PROBLEM
#     )

#     tc._publish_channel.basic_publish(
#         exchange=tc._publish_exchange,
#         routing_key="json.dwgps_gnr.crap.gnf.dwgps_gnf",
#         body=payload.as_type(),
#         properties=properties,
#     )
#     wait_for(
#         lambda: supervisor.messages_received == 6, 2, f"gnf.messages_received is {supervisor.messages_received}"
#     )
#     assert supervisor.messages_received == 6
#     assert supervisor.messages_routed_internally == 0
#     assert (
#         supervisor._latest_on_message_diagnostic == OnReceiveMessageDiagnostic.FROM_GNODE_DECODING_PROBLEM
#     )

#     supervisor._consume_channel.queue_unbind(
#         supervisor.queue_name,
#         "gnrmic_tx",
#         routing_key="garbage.#",
#     )
#     supervisor._consume_channel.queue_unbind(
#         supervisor.queue_name,
#         "gnrmic_tx",
#         routing_key="pubsub.#",
#     )
#     supervisor._consume_channel.queue_unbind(
#         supervisor.queue_name,
#         "gnrmic_tx",
#         routing_key="json",
#     )
#     supervisor._consume_channel.queue_unbind(
#         supervisor.queue_name,
#         "gnrmic_tx",
#         routing_key="json.*.crap.*.*",
#     )

#     ####################################
#     # Testing actor_base.send_direct_message
#     ###################################

#     supervisor._stopping = True
#     result = supervisor.send_direct_message(
#         payload=payload, to_g_node_type_short_alias="gnr", to_g_node_alias="dwgps.gnr"
#     )
#     assert result == OnSendMessageDiagnostic.STOPPING_SO_NOT_SENDING
#     supervisor._stopping = False

#     supervisor._publish_channel.close()

#     supervisor._publish_channel = None
#     result = supervisor.send_direct_message(
#         payload=payload,
#         to_g_node_type_short_alias="gnr",
#         to_g_node_alias="dwgps.gnr",
#     )
#     assert result == OnSendMessageDiagnostic.CHANNEL_NOT_OPEN

#     supervisor._publish_channel = None
#     result = supervisor.send_direct_message(
#         payload=payload,
#         to_g_node_type_short_alias="gnr",
#         to_g_node_alias="dwgps.gnr",
#     )
#     assert result == OnSendMessageDiagnostic.CHANNEL_NOT_OPEN

#     tc.stop()
#     supervisor.stop()
