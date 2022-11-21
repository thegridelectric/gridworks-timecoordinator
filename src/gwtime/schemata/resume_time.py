"""Type resume.time, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal

from pydantic import BaseModel

import gwtime.property_format as property_format
from gwtime.errors import SchemaError
from gwtime.property_format import predicate_validator


class ResumeTime(BaseModel):
    FromGNodeAlias: str  #
    FromGNodeInstanceId: str  #
    ToGNodeAlias: str  #
    TypeName: Literal["resume.time"] = "resume.time"
    Version: str = "000"

    _validator_from_g_node_alias = predicate_validator(
        "FromGNodeAlias", property_format.is_lrd_alias_format
    )

    _validator_from_g_node_instance_id = predicate_validator(
        "FromGNodeInstanceId", property_format.is_uuid_canonical_textual
    )

    _validator_to_g_node_alias = predicate_validator(
        "ToGNodeAlias", property_format.is_lrd_alias_format
    )

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())


class ResumeTime_Maker:
    type_name = "resume.time"
    version = "000"

    def __init__(
        self, from_g_node_alias: str, from_g_node_instance_id: str, to_g_node_alias: str
    ):

        self.tuple = ResumeTime(
            FromGNodeAlias=from_g_node_alias,
            FromGNodeInstanceId=from_g_node_instance_id,
            ToGNodeAlias=to_g_node_alias,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: ResumeTime) -> str:
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> ResumeTime:
        try:
            d = json.loads(t)
        except TypeError:
            raise SchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise SchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> ResumeTime:
        d2 = dict(d)
        if "FromGNodeAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FromGNodeAlias")
        if "FromGNodeInstanceId" not in d2.keys():
            raise SchemaError(f"dict {d2} missing FromGNodeInstanceId")
        if "ToGNodeAlias" not in d2.keys():
            raise SchemaError(f"dict {d2} missing ToGNodeAlias")
        if "TypeName" not in d2.keys():
            raise SchemaError(f"dict {d2} missing TypeName")

        return ResumeTime(
            FromGNodeAlias=d2["FromGNodeAlias"],
            FromGNodeInstanceId=d2["FromGNodeInstanceId"],
            ToGNodeAlias=d2["ToGNodeAlias"],
            TypeName=d2["TypeName"],
            Version="000",
        )
