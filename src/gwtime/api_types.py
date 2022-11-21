""" List of all the types used"""
from typing import Dict
from typing import List
from typing import no_type_check

from gwtime.schemata import HeartbeatA_Maker
from gwtime.schemata import PauseTime_Maker
from gwtime.schemata import Ready_Maker
from gwtime.schemata import ResumeTime_Maker
from gwtime.schemata import SimTimestep_Maker


TypeMakerByName: Dict[str, HeartbeatA_Maker] = {}


@no_type_check
def type_makers() -> List[HeartbeatA_Maker]:
    return [
        HeartbeatA_Maker,
        PauseTime_Maker,
        Ready_Maker,
        ResumeTime_Maker,
        SimTimestep_Maker,
    ]


for maker in type_makers():
    TypeMakerByName[maker.type_name] = maker


def version_by_type_name() -> Dict[str, str]:
    """
    Returns:
        Dict[str, str]: Keys are TypeNames, values are versions
    """

    v: Dict[str, str] = {
        "heartbeat.a": "000",
        "pause.time": "000",
        "ready": "000",
        "resume.time": "000",
        "sim.timestep": "000",
    }

    return v


def status_by_versioned_type_name() -> Dict[str, str]:
    """
    Returns:
        Dict[str, str]: Keys are versioned TypeNames, values are type status
    """

    v: Dict[str, str] = {
        "heartbeat.a.000": "Pending",
        "pause.time.000": "Pending",
        "ready.000": "Pending",
        "resume.time.000": "Pending",
        "sim.timestep.000": "Pending",
    }

    return v
