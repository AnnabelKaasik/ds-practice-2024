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

utils_path3 = os.path.abspath(os.path.join(FILE, '../../../utils/pb/database'))
sys.path.insert(0, utils_path3)
import database_pb2 as database
import database_pb2_grpc as database_grpc

import grpc
from concurrent import futures
import random

this_node = ""
leader = "0"

def leader_loop():
    while True:
        with grpc.insecure_channel(f'order_queue:50054') as channel:
            stub = order_queue_grpc.OrderQueueServiceStub(channel)
            new_order = stub.DequeueOrder(order_queue.DequeueRequest(executor_id=str(this_node)))
            if new_order.success:
                executor_order = order_executor.Order(orderId=new_order.order.orderId, userName=new_order.order.userName, bookTitle=new_order.order.bookTitle, quantity=new_order.order.quantity)
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
    def __init__(self):
        # Master database service address for writes
        self.master_address = 'master:50057'
        print(f"LOG: Connecting to master database at {self.master_address}")
        self.database_stub = database_grpc.BookDatabaseStub(grpc.insecure_channel(self.master_address))


    def get_master_stub(self):
        channel = grpc.insecure_channel('master:50057')
        return database_grpc.BookDatabaseStub(channel)


    def ProcessOrder(self, request, context):
    # Use a slave stub for reading current stock
        print("LOG: Order executor service called in function ProcessOrder.")
        book_title = request.order.bookTitle
        quantity = request.order.quantity

         # Testing code:kustuta pärast ära
        print("enne with")
        with grpc.insecure_channel(f'master:50057') as channel:
                stub = self.get_master_stub()
                print("stub", stub)
                testing = database.BookRead(title=book_title)
                print("testing", testing)
                # Siin on midagi perses
                response = stub.Read(database.BookRead(title=book_title))
                print("with shit response", response)

        try:
            # Check current stock from the database from master
          
            # THis is not working
            current_stock_response = self.database_stub.Read(database.BookRead(title=book_title))
            current_stock = current_stock_response.stock
            print(f"LOG: Current stock for {book_title} is {current_stock}")

            if current_stock >= quantity:
                # If stock is available, use master to update the database
                new_stock = current_stock - quantity
                print(f"LOG: Attempting to update stock for {book_title} to {new_stock}")
                update_response = self.database_stub.Write(database.BookWrite(title=book_title, newStock=new_stock))

                if update_response.success:
                    print(f"LOG: Database updated successfully for {book_title}")
                    return order_executor.DequeueResponse(order_received=True, message="Order processed successfully")
                else:
                    print(f"ERROR: Failed to update the stock for {book_title}")
                    return order_executor.DequeueResponse(order_received=False, message="Failed to update the stock")
            else:
                print(f"LOG: Insufficient stock for {book_title}")
                return order_executor.DequeueResponse(order_received=False, message="Insufficient stock")

        except grpc.RpcError as e:
            print(f"ERROR: gRPC call failed with {e.code()}: {e.details()}")
            return order_executor.DequeueResponse(order_received=False, message="Failed due to internal server error")


    def Dequeue(self, request, context):
        try:
            print("LOG: Order executor service called in function Dequeue.")
            print(f"Order Details - ID: {request.order.orderId}, User: {request.order.userName}, Book: {request.order.bookTitle}, Quantity: {request.order.quantity}")
             
            # Directly calling ProcessOrder here after dequeuing
            print("request", request)  
            process_response = self.ProcessOrder(request, context)
            print(f"Processing Response: {process_response.message}") 
            print("process_response", process_response)  
            # return self.ProcessOrder(request, context)
            return order_executor.DequeueResponse(order_received=True, message="Order processed successfully")
        except Exception as e:
            print(f"ERROR: Exception in Dequeue: {e}")
            return order_executor.DequeueResponse(order_received=False, message="Failed to process order")
        finally:
            print(f"LOG: Order received: {request.order}")
            time.sleep(30)


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
    