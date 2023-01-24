"""Settings for an TimeCoordinator, readable from environment and/or from env files."""

import pendulum
from gridworks.gw_config import GNodeSettings


DEFAULT_ENV_FILE = ".env"


class Settings(GNodeSettings):
    g_node_alias: str = "d1.time"
    g_node_id: str = "d4057686-c199-4274-b595-f7e39ce863e2"
    g_node_instance_id: str = "a8b49455-85de-461f-9bf6-1b831c11c5d1"
    g_node_role_value: str = "TimeCoordinator"
    my_super_alias = "d1.super1"
    initial_time_unix_s = pendulum.datetime(
        year=2020, month=1, day=1, hour=5
    ).int_timestamp
    time_step_duration_s = 3600
    my_time_coordinator_alias = "d1.time"
    log_level: str = "INFO"

    class Config:
        env_prefix = "TC_"
        env_nested_delimiter = "__"
