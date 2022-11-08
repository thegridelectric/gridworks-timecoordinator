"""Type ready, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal

from pydantic import BaseModel

import gwtime.property_format as property_format
from gwtime.errors import SchemaError
from gwtime.property_format import predicate_validator


class Ready(BaseModel):
    FromGNodeAlias: str  #
    FromGNodeInstanceId: str  #
    TypeName: Literal["ready"] = "ready"
    Version: str = "000"

    _validator_from_g_node_alias = predicate_validator(
        "FromGNodeAlias", property_format.is_lrd_alias_format
    )

    _validator_from_g_node_instance_id = predicate_validator(
        "FromGNodeInstanceId", property_format.is_uuid_canonical_textual
    )

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class Ready_Maker:
    type_name = "ready"
    version = "000"

    def __init__(self, from_g_node_alias: str, from_g_node_instance_id: str):

        self.tuple = Ready(
            FromGNodeAlias=from_g_node_alias,
            FromGNodeInstanceId=from_g_node_instance_id,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: Ready) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> Ready:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> Ready:
        d2 = dict(d)
        if "FromGNodeAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FromGNodeAlias")
        if "FromGNodeInstanceId" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FromGNodeInstanceId")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return Ready(
            FromGNodeAlias=d2["FromGNodeAlias"],
            FromGNodeInstanceId=d2["FromGNodeInstanceId"],
            TypeName=d2["TypeName"],
            Version="000",
        )
