"""Tests for schema enum message.category.symbol.000"""
from gwtime.enums import MessageCategorySymbol


def test_message_category_symbol() -> None:

    assert set(MessageCategorySymbol.values()) == {
        "unknown",
        "rj",
        "rjb",
        "s",
        "gw",
        "post",
        "postack",
        "get",
    }

    assert MessageCategorySymbol.default() == MessageCategorySymbol.unknown
