import os
import sys
import grpc
from concurrent import futures
import json




FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/database'))
sys.path.insert(0, utils_path)
import database_pb2 as database
import database_pb2_grpc as database_grpc

class BookDatabaseService(database_grpc.BookDatabaseServicer):
    def __init__(self):
        self.book_stock = {}  # Start with an empty dictionary
        self.is_master = os.getenv("IS_MASTER", "false").lower() == 'true'
        self.initialize_book_stock()

    def initialize_book_stock(self):
        books_data = {
            "Learning Python": 7,
            "JavaScript - The Good Parts": 15,
            "Domain-Driven Design: Tackling Complexity in the Heart of Software": 15,
            "Design Patterns: Elements of Reusable Object-Oriented Software": 15,
        }
        self.book_stock.update(books_data)
        print("LOG: Book stock initialized:", self.book_stock)

    def Read(self, request, context):
        print(f"LOG: Received read request: {request.title}")
        if request.title not in self.book_stock:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Book not found: {request.title}")
            return database.BookStock()
        else:
            stock = self.book_stock[request.title]
            return database.BookStock(title=request.title, stock=stock)
        
    def check_Write(self, request, context):
        print(f"LOG: Received write request: {request.title} - {request.newStock}")
        if not self.is_master:
            return database.UpdateAck(success=False, message="Write operation not allowed on slave.")
        if not request.title:
            return database.UpdateAck(success=False, message="Title missing in request.")
        if not request.newStock:
            return database.UpdateAck(success=False, message="New stock missing in request.")
        return database.UpdateAck(success=True, message="Check passed. Write operation allowed on master.")

    def Write(self, request, context):
        if self.is_master:
            self.book_stock[request.title] = request.newStock
            success = self.update_slaves(request)
            if success:
                return database.UpdateAck(success=True, message="Stock updated successfully and propagated to slaves.")
            # return database.UpdateAck(success=True, message="Stock updated successfully.")
            return database.UpdateAck(success=False, message="Update successful on master, but failed to propagate to one or more slaves.")
        return database.UpdateAck(success=False, message="Write operation not allowed on slave.")
    

    def update_slaves(self, request):
        print("LOG: Propagating update to slaves")
        success = True
        slave_addresses = ['slave_1:50058', 'slave_2:50059']
        
        for address in slave_addresses:
            try:
                stub = database_grpc.BookDatabaseStub(grpc.insecure_channel(address))
                stub.Write(database.BookWrite(title=request.title, newStock=request.newStock))
                print(f"LOG: Updated {address} for {request.title} to {request.newStock}")
                
            except grpc.RpcError as e:
                print(f"LOG: Failed to update slave: {e}")
                success = False
        return success



def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    service = BookDatabaseService()
    database_grpc.add_BookDatabaseServicer_to_server(service, server)
    port = os.getenv('LISTENING_PORT')
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Server started on port {port}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()