import sys
import os
from collections import deque


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
leader = "50058"
number_of_nodes = 3
this_node = 50054

def call_all_executors():
    for i in range(50058, 50058 + number_of_nodes):
        with grpc.insecure_channel(f'order_executor:{i}') as channel:
            stub = order_executor_grpc.OrderExecutorServiceStub(channel)
            response = stub.Are_You_Available(order_executor.Are_You_AvailableRequest(request_from_id = str(this_node),
                                                                                      leader_id = str(leader),
                                                                                      request_to_id = str(i)))
            print(f"LOG: Executor {i} is available: {response.available}")
    


class OrderQueueService(order_queue_grpc.OrderQueueServiceServicer):
    def EnqueueOrder(self, request, context):
        print("LOG: Order queue service called.")
        order_queue_list.append(request)
        print(f"LOG: Order enqueued: {order_queue_list}")
        return order_queue.EnqueueResponse(success = True, message="Order enqueued")
    
    
    def DequeueOrder(self, request, context):
        print("LOG: Order queue service called.")
        if order_queue_list:
            print(f"LOG: Order dequeued: {order_queue_list}")
            return order_queue.DequeueResponse(success = True, order=order_queue_list.pop())
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
    
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
    call_all_executors()