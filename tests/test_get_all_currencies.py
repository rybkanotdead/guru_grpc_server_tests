"""Tests for GetAllCurrencies gRPC method."""

from google.protobuf import empty_pb2

from internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient


def test_get_all_currencies(grpc_client: NifflerCurrencyServiceClient) -> None:
    """
    Test that GetAllCurrencies returns all supported currencies.

    Expected behavior:
        - Returns 4 currencies: RUB, USD, EUR, KZT
        - Each currency has a currency code and exchange rate
    """
    # Call GetAllCurrencies with empty request
    response = grpc_client.get_all_currencies(empty_pb2.Empty())

    # Validate response
    assert len(response.allCurrencies) == 4, (
        f"Expected 4 currencies, got {len(response.allCurrencies)}"
    )

    # Validate that all currencies have required fields
    for currency in response.allCurrencies:
        assert currency.currency is not None, "Currency code should be set"
        assert currency.currencyRate > 0, "Currency rate should be positive"
