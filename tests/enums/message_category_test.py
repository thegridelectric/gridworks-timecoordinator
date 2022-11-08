"""Tests for schema enum message.category.000"""
from gwtime.enums import MessageCategory


def test_message_category() -> None:

    assert set(MessageCategory.values()) == {
        "Unknown",
        "RabbitJsonDirect",
        "RabbitJsonBroadcast",
        "RabbitGwSerial",
        "MqttJsonBroadcast",
        "RestApiPost",
        "RestApiPostResponse",
        "RestApiGet",
    }

    assert MessageCategory.default() == MessageCategory.Unknown
