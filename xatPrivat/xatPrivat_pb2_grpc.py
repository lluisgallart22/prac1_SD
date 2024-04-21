# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import xatPrivat_pb2 as xatPrivat__pb2


class XatStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendMessage = channel.unary_stream(
                '/Xat/SendMessage',
                request_serializer=xatPrivat__pb2.MessageRequest.SerializeToString,
                response_deserializer=xatPrivat__pb2.MessageResponse.FromString,
                )


class XatServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SendMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_XatServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendMessage': grpc.unary_stream_rpc_method_handler(
                    servicer.SendMessage,
                    request_deserializer=xatPrivat__pb2.MessageRequest.FromString,
                    response_serializer=xatPrivat__pb2.MessageResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Xat', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Xat(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SendMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/Xat/SendMessage',
            xatPrivat__pb2.MessageRequest.SerializeToString,
            xatPrivat__pb2.MessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
