from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings for gRPC service hosts."""

    wiremock_host: str = Field(
        default="localhost:8094",
        alias="WIREMOCK_HOST",
        description="WireMock mock service host"
    )
    currency_service_host: str = Field(
        default="localhost:8092",
        alias="CURRENCY_SERVICE_HOST",
        description="Niffler currency service host"
    )
