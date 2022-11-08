"""Settings for an TimeCoordinator, readable from environment and/or from env files."""

from pydantic import BaseModel
from pydantic import BaseSettings
from pydantic import SecretStr


DEFAULT_ENV_FILE = ".env"


class RabbitBrokerClient(BaseModel):
    """Settings for connecting to a Rabbit Broker"""

    url: SecretStr = SecretStr("amqp://smqPublic:smqPublic@localhost:5672/dw1__1")
    role_value: str = "timecoordinator"


class Settings(BaseSettings):

    g_node_alias: str = "dw1.tc"
    g_node_id: str = "d4057686-c199-4274-b595-f7e39ce863e2"
    g_node_instance_id: str = "'a8b49455-85de-461f-9bf6-1b831c11c5d1"
    log_level: str = "WARNING"
    universe: str = "dev"
    rabbit: RabbitBrokerClient = RabbitBrokerClient()

    class Config:
        env_prefix = "TC_"
        env_nested_delimiter = "__"


#### Below is just for stubbing out a dev Validator account that does
# not have access to Gnf secrets
