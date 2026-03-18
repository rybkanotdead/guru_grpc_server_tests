"""gRPC interceptor for logging requests and responses to console."""

from typing import Callable

import grpc
from google.protobuf.message import Message


class LoggingInterceptor(grpc.UnaryUnaryClientInterceptor):
    """Interceptor that logs gRPC method calls and their results."""

    def intercept_unary_unary(
        self,
        continuation: Callable,
        client_call_details: grpc.ClientCallDetails,
        request: Message,
    ) -> Callable:
        """
        Intercept unary-unary gRPC calls to log request and response.

        Args:
            continuation: Next interceptor or actual RPC call
            client_call_details: Details about the RPC call
            request: Request message

        Returns:
            Response from the RPC call
        """
        print(f"[gRPC Request] {client_call_details.method}")
        print(f"[Request Body] {request}")

        response = continuation(client_call_details, request)

        print(f"[Response Body] {response.result()}")

        return response
