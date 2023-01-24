""" List of all the types used"""
from typing import Dict
from typing import List
from typing import no_type_check

from gwtime.types import DebugTcReinitializeTime_Maker
from gwtime.types import HeartbeatA_Maker
from gwtime.types import PauseTime_Maker
from gwtime.types import Ready_Maker
from gwtime.types import ResumeTime_Maker
from gwtime.types import SimTimestep_Maker


TypeMakerByName: Dict[str, HeartbeatA_Maker] = {}


@no_type_check
def type_makers() -> List[HeartbeatA_Maker]:
    return [
        DebugTcReinitializeTime_Maker,
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
        "debug.tc.reinitialize.time": "000",
        "heartbeat.a": "100",
        "pause.time": "000",
        "ready": "001",
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
        "debug.tc.reinitialize.time.000": "Pending",
        "heartbeat.a.100": "Pending",
        "pause.time.000": "Pending",
        "ready.001": "Pending",
        "resume.time.000": "Pending",
        "sim.timestep.000": "Pending",
    }

    return v
