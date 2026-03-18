"""Pytest configuration and fixtures for gRPC tests."""

import pytest
import grpc
from grpc import insecure_channel

from internal.grpc.interceptors.allure import AllureInterceptor
from internal.grpc.interceptors.logging import LoggingInterceptor
from internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient
from settings.settings import Settings

# List of interceptors to apply to all gRPC calls
INTERCEPTORS = [
    LoggingInterceptor(),
    AllureInterceptor(),
]


@pytest.fixture(scope="session")
def settings() -> Settings:
    """
    Fixture that provides application settings.

    Returns:
        Settings instance with configured service hosts
    """
    return Settings()


def pytest_addoption(parser: pytest.Parser) -> None:
    """
    Add custom command-line options to pytest.

    Args:
        parser: pytest Parser instance
    """
    parser.addoption(
        "--mock",
        action="store_true",
        default=False,
        help="Run tests against WireMock instead of real service",
    )


@pytest.fixture(scope="session")
def grpc_client(
    settings: Settings, request: pytest.FixtureRequest
) -> NifflerCurrencyServiceClient:
    """
    Fixture that provides gRPC client with interceptors.

    The client connects to either the real service or WireMock
    depending on the --mock command-line flag.

    Args:
        settings: Application settings
        request: pytest FixtureRequest to access command-line options

    Returns:
        Configured NifflerCurrencyServiceClient instance
    """
    # Select host based on --mock flag
    host = settings.currency_service_host
    if request.config.getoption("--mock"):
        host = settings.wiremock_host

    # Create insecure channel (no TLS)
    channel = insecure_channel(host)

    # Apply interceptors to channel
    intercept_channel = grpc.intercept_channel(channel, *INTERCEPTORS)

    # Return client with intercepted channel
    return NifflerCurrencyServiceClient(intercept_channel)
