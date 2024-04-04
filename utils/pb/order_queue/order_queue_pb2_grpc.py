# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import order_queue_pb2 as order__queue__pb2


class OrderQueueServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.EnqueueOrder = channel.unary_unary(
                '/orderqueue.OrderQueueService/EnqueueOrder',
                request_serializer=order__queue__pb2.EnqueueRequest.SerializeToString,
                response_deserializer=order__queue__pb2.EnqueueResponse.FromString,
                )
        self.DequeueOrder = channel.unary_unary(
                '/orderqueue.OrderQueueService/DequeueOrder',
                request_serializer=order__queue__pb2.DequeueRequest.SerializeToString,
                response_deserializer=order__queue__pb2.DequeueResponse.FromString,
                )


class OrderQueueServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def EnqueueOrder(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DequeueOrder(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OrderQueueServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'EnqueueOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.EnqueueOrder,
                    request_deserializer=order__queue__pb2.EnqueueRequest.FromString,
                    response_serializer=order__queue__pb2.EnqueueResponse.SerializeToString,
            ),
            'DequeueOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.DequeueOrder,
                    request_deserializer=order__queue__pb2.DequeueRequest.FromString,
                    response_serializer=order__queue__pb2.DequeueResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'orderqueue.OrderQueueService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class OrderQueueService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def EnqueueOrder(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/orderqueue.OrderQueueService/EnqueueOrder',
            order__queue__pb2.EnqueueRequest.SerializeToString,
            order__queue__pb2.EnqueueResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DequeueOrder(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/orderqueue.OrderQueueService/DequeueOrder',
            order__queue__pb2.DequeueRequest.SerializeToString,
            order__queue__pb2.DequeueResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
