import sys
import os
from collections import deque


# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_executor'))
sys.path.insert(0, utils_path)
import order_executor_pb2 as order_executor
import order_executor_pb2_grpc as order_executor_grpc

utils_path2 = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_queue'))
sys.path.insert(0, utils_path2)
import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc

import grpc
from concurrent import futures

this_node = ""

class OrderExecutorService(order_executor_grpc.OrderExecutorServiceServicer):

    def Dequeue(self, request, context):

        with grpc.insecure_channel('order_queue:50054') as channel:
            stub = order_queue_grpc.OrderQueueServiceStub(channel)
            response = stub.DequeueOrder(order_queue.DequeueRequest(executor_id=str(1)))
            if response.success:
                print(f"LOG: Order dequeued: {response.order}")
                return order_executor.DequeueResponse(sendind_an_order = True, order=response.order)
        
        return order_executor.DequeueResponse(sendind_an_order = False)
    


    def Are_You_Available(self, request, context):
        print("LOG: Order executor service called.")
        global this_node
        this_node = request.request_to_id
        
        return order_executor.Are_You_AvailableResponse(executor_id= context)
    
def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    order_executor_grpc.add_OrderExecutorServiceServicer_to_server(OrderExecutorService(), server)
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
    