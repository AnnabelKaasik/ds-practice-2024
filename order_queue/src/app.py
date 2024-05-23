import sys
import os
from collections import deque
import time
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# Service name is required for most backends
resource = Resource(attributes={
    SERVICE_NAME: "observability"
})

traceProvider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://observability:4318/v1/traces"))
traceProvider.add_span_processor(processor)
trace.set_tracer_provider(traceProvider)

reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://observability:4318/v1/metrics")
)
meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meterProvider)

meter = metrics.get_meter("queue")


tracer = trace.get_tracer("traces.form.order_queue")



# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_queue'))
sys.path.insert(0, utils_path)
import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc

utils_path2 = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_executor'))
sys.path.insert(0, utils_path2)
import order_executor_pb2 as order_executor
import order_executor_pb2_grpc as order_executor_grpc


import grpc
from concurrent import futures

order_queue_list = deque()
leader = "50055"
number_of_nodes = 1
this_node = 50054


def get_queue_length(_: metrics.CallbackOptions):
    yield metrics.Observation(len(order_queue_list))


queue_size_gauge = meter.create_observable_gauge(
        name="queue_length_gauge",
        description="queue length",
        unit="orders",
        callbacks=[get_queue_length]
    )

def get_number_of_nodes(_: metrics.CallbackOptions):
    yield metrics.Observation(number_of_nodes)


number_of_nodes_gauge = meter.create_observable_gauge(
        name="number_of_executors_gauge",
        description="number of executors",
        unit="executors",
        callbacks=[get_number_of_nodes]
    )



def call_all_executors():
    for j,i in zip(range(1,number_of_nodes+1),range(50055, 50055 + number_of_nodes)):
        with grpc.insecure_channel(f'ds-practice-2024-order_executor-{j}:{i}') as channel:
            stub = order_executor_grpc.OrderExecutorServiceStub(channel)
            response = stub.Are_You_Available(order_executor.Are_You_AvailableRequest(request_from_id = str(this_node),
                                                                                      leader_id = str(leader),
                                                                                      request_to_id = str(i)))
            print(f"LOG: Executor {i} is available: {response.available}")
    


class OrderQueueService(order_queue_grpc.OrderQueueServiceServicer):
    def EnqueueOrder(self, request, context):
        print("LOG: Order queue service called.")
        
        
        with tracer.start_as_current_span("new_order_to_queue") as span:
            span.set_attribute("data", str(request))
        
        order_queue_list.append(request)
        # Log the entire queue or the latest enqueued order to verify
        print(f"LOG: Order enqueued: ID: {request.order}")

        return order_queue.EnqueueResponse(success = True, message="Order enqueued")
    
    
    def DequeueOrder(self, request, context):
        print("LOG: Order queue service called. There are currently", len(order_queue_list), "orders in the queue.")

        if order_queue_list:
            print(f"LOG: Order dequeued: {order_queue_list}")
            order  = order_queue_list.pop()
            return order_queue.DequeueResponse(success = True, order=order_queue.Order(
                orderId = order.order.orderId, 
                userName = order.order.userName,
                bookTitle=order.order.bookTitle,   # Added book name ans quantity
                quantity=order.order.quantity
                ))
        return order_queue.DequeueResponse(success = False)

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    order_queue_grpc.add_OrderQueueServiceServicer_to_server(OrderQueueService(), server)
    # Listen on port 50054
    port = "50054"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Server started. Listening on port 50054.")    
    time.sleep(5)
    call_all_executors()
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
