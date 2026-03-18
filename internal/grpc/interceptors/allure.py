"""gRPC interceptor for Allure report attachments."""

from typing import Callable

import allure
import grpc
from google.protobuf.message import Message
from google.protobuf.json_format import MessageToJson


class AllureInterceptor(grpc.UnaryUnaryClientInterceptor):
    """Interceptor that attaches gRPC requests/responses to Allure reports."""

    def intercept_unary_unary(
        self,
        continuation: Callable,
        client_call_details: grpc.ClientCallDetails,
        request: Message,
    ) -> Callable:
        """
        Intercept unary-unary gRPC calls to attach data to Allure report.

        Args:
            continuation: Next interceptor or actual RPC call
            client_call_details: Details about the RPC call
            request: Request message

        Returns:
            Response from the RPC call
        """
        with allure.step(client_call_details.method):
            # Attach request as JSON
            allure.attach(
                MessageToJson(request),
                "request",
                attachment_type=allure.attachment_type.JSON,
            )

            # Execute the RPC call
            response = continuation(client_call_details, request)

            # Attach response as JSON
            allure.attach(
                MessageToJson(response.result()),
                "response",
                attachment_type=allure.attachment_type.JSON,
            )

        return response
