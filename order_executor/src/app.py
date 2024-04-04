import sys
import os
from collections import deque
import time

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
leader = "0"

def leader_loop():
    while True:
        with grpc.insecure_channel(f'order_queue:50054') as channel:
            stub = order_queue_grpc.OrderQueueServiceStub(channel)
            new_order = stub.DequeueOrder(order_queue.DequeueRequest(executor_id=str(this_node)))
            if new_order.success:
                executor_order = order_executor.Order(orderId=new_order.order.orderId, userName=new_order.order.userName)
                for i in range(50056, 50056 + 1):
                    with grpc.insecure_channel(f'order_executor_2:{i}') as channel:
                        stub = order_executor_grpc.OrderExecutorServiceStub(channel)
                        response = stub.Dequeue(order_executor.DequeueRequest(order=executor_order))
                        if response.order_received:
                            print(f"LOG: Order sent to executor {i}")
                            break
            else:
                time.sleep(5)
    

class OrderExecutorService(order_executor_grpc.OrderExecutorServiceServicer):

    def Dequeue(self, request, context):
        try:
            print("LOG: Order executor service called in function Dequeue.")
            return order_executor.DequeueResponse(order_received=True)
        except Exception as e:
            print(f"ERROR: Exception in Dequeue: {e}")
            return order_executor.DequeueResponse(order_received=False)
        finally:
            print(f"LOG: Order received: {request.order}")
            time.sleep(10)


    def Are_You_Available(self, request, context):
        try:
            print("LOG: Order executor service called.")
            global this_node
            global leader
            leader = request.leader_id
            this_node = request.request_to_id
            print(leader, this_node)
            return order_executor.Are_You_AvailableResponse(executor_id=this_node,
                                                            leader_id=leader,
                                                            available=True)
        except Exception as e:
            print(f"ERROR: Exception in Are_You_Available: {e}")
            return order_executor.Are_You_AvailableResponse(available=False)
        finally:
            if leader == this_node:
                leader_loop()        
    
def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    order_executor_grpc.add_OrderExecutorServiceServicer_to_server(OrderExecutorService(), server)
    # Listen on port 50055
    port = os.getenv("LISTENING_PORT", "50055")
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print(f"Server started. Listening on port {port}.")

    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
    