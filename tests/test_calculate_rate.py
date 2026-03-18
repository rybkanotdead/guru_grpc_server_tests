"""Tests for CalculateRate gRPC method."""

import grpc
import pytest

from internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient
from internal.pb.niffler_currency_pb2 import CalculateRequest, CurrencyValues


def test_calculate_rate_eur_to_rub(grpc_client: NifflerCurrencyServiceClient) -> None:
    """
    Test currency conversion from EUR to RUB.

    Expected behavior:
        - 100 EUR = 7200 RUB (at rate 1 EUR = 72 RUB)
    """
    response = grpc_client.calculate_rate(
        request=CalculateRequest(
            spendCurrency=CurrencyValues.EUR,
            desiredCurrency=CurrencyValues.RUB,
            amount=100,
        )
    )

    assert response.calculatedAmount == 7200, (
        f"Expected 7200 RUB, got {response.calculatedAmount}"
    )


def test_calculate_rate_without_desired_currency(
    grpc_client: NifflerCurrencyServiceClient,
) -> None:
    """
    Test that missing desiredCurrency field returns an error.

    Expected behavior:
        - Should return gRPC error with UNKNOWN status
        - Error message: "Application error processing RPC"
    """
    try:
        grpc_client.calculate_rate(
            request=CalculateRequest(
                spendCurrency=CurrencyValues.EUR,
                amount=100,
            )
        )
        pytest.fail("Expected RpcError but got successful response")
    except grpc.RpcError as e:
        assert e.code() == grpc.StatusCode.UNKNOWN, (
            f"Expected UNKNOWN status, got {e.code()}"
        )
        assert e.details() == "Application error processing RPC", (
            f"Expected specific error message, got: {e.details()}"
        )


@pytest.mark.parametrize(
    "spend,spend_currency,desired_currency,expected_result",
    [
        (100.0, CurrencyValues.USD, CurrencyValues.RUB, 6666.67),
        (100.0, CurrencyValues.RUB, CurrencyValues.USD, 1.5),
        (100.0, CurrencyValues.USD, CurrencyValues.USD, 100.0),
    ],
    ids=[
        "USD to RUB conversion",
        "RUB to USD conversion",
        "Same currency (USD to USD)",
    ],
)
def test_currency_conversion(
    grpc_client: NifflerCurrencyServiceClient,
    spend: float,
    spend_currency: CurrencyValues,
    desired_currency: CurrencyValues,
    expected_result: float,
) -> None:
    """
    Parametrized test for various currency conversion scenarios.

    Args:
        grpc_client: gRPC client fixture
        spend: Amount to convert
        spend_currency: Source currency
        desired_currency: Target currency
        expected_result: Expected converted amount
    """
    response = grpc_client.calculate_rate(
        request=CalculateRequest(
            spendCurrency=spend_currency,
            desiredCurrency=desired_currency,
            amount=spend,
        )
    )

    assert response.calculatedAmount == expected_result, (
        f"Expected {expected_result}, got {response.calculatedAmount}"
    )
