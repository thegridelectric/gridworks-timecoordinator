

SDK for `gridworks-atn <https://pypi.org/project/gridworks-atn/>`_  Types
===========================================================================

The Python classes enumerated below provide an interpretation of gridworks-atn
type instances (serialized JSON) as Python objects. Types are the building
blocks for all GridWorks APIs. You can read more about how they work
`here <https://gridworks.readthedocs.io/en/latest/api-sdk-abi.html>`_, and
examine their API specifications `here <apis/types.html>`_.
The Python classes below also come with methods for translating back and
forth between type instances and Python objects.


.. automodule:: gwtime.types

.. toctree::
   :maxdepth: 1
   :caption: TYPE SDKS

    DebugTcReinitializeTime  <types/debug-tc-reinitialize-time>
    HeartbeatA  <types/heartbeat-a>
    PauseTime  <types/pause-time>
    Ready  <types/ready>
    ResumeTime  <types/resume-time>
    SimTimestep  <types/sim-timestep>
