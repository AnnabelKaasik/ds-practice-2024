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


# class BookDatabaseService(database_grpc.BookDatabaseServicer):
#     def __init__(self):
#         # Start with an empty dictionary
#         self.book_stock = {}
#         # Determine if this instance is master
#         self.is_master = os.getenv("IS_MASTER", "false").lower() == 'true'

#         books_data = {
#             "book1": {
#                 "id": "1",
#                 "title": "Learning Python",
#                 "author": "John Smith",
#                 "description": "An in-depth guide to Python programming.",
#                 "copies": 10,
#                 "copiesAvailable": 7,
#                 "category": "Programming",
#                 "img": "https://m.media-amazon.com/images/W/MEDIAX_792452-T1/images/I/51FD3C3kLiL.jpg",
#                 "price": 3
#             },
#             "book2": {
#                 "id": "2",
#                 "title": "JavaScript - The Good Parts",
#                 "author": "Jane Doe",
#                 "description": "Unearthing the excellence in JavaScript.",
#                 "copies": 15,
#                 "copiesAvailable": 15,
#                 "category": "Web Development",
#                 "img": "https://m.media-amazon.com/images/W/MEDIAX_792452-T1/images/I/91YlBt-bCHL._SL1500_.jpg",
#                 "price": 3
#             }
#         }
#         if self.is_master:
#             print("Running as MASTER node")
#             self.initialize_book_stock(books_data)
#             # self.slave_addresses = [
#             #     'slave_1:50058',
#             #     'slave_2:50059'
#             # ]
#             # self.slaves = []
#             # self.initialize_slaves()
           

#         else:
#             print("Running as SLAVE node")

#     # def initialize_slaves(self):
#     #     """Initialize communication stubs to all configured slave addresses."""
#     #     for address in self.slave_addresses:
#     #         channel = grpc.insecure_channel(address)
#     #         stub = database_grpc.BookDatabaseStub(channel)
#     #         self.slaves.append(stub)
#     #         print(f"Connected to slave at {address}")

#     def initialize_book_stock(self, books_data):
#         for book_id, book_info in books_data.items():
#             self.book_stock[book_info['title']] = book_info['copiesAvailable']
#         print("Book stock initialized:", self.book_stock)

#     def Read(self, request, context):
#         stock = self.book_stock.get(request.title, 0)
#         return database.BookStock(title=request.title, stock=stock)

#     def Write(self, request, context):
#         print(f"Received write request: {request.title} - {request.newStock}")
#         print(self.is_master)
#         if self.is_master:
#             self.book_stock[request.title] = request.newStock
#             print(f"Updated {request.title} stock to {request.newStock} on master.")
#             success = self.update_slaves(request)
#             if success:
#                 return database.UpdateAck(success=True, message="Update successful and propagated to slaves.")
#             else:
#                 return database.UpdateAck(success=False, message="Update successful on master, but failed to propagate to one or more slaves.")
#         else:
#             return database.UpdateAck(success=False, message="Write not allowed on slave.")

#     def update_slaves(self, request):
#         """send the update to all connected slave nodes."""
#         print("Propagating update to slaves")
#         success = True
#         slave_addresses = ['ds-practice-2024-slave_1:50058', 'ds-practice-2024-slave_2:50059']
        
#         for address in slave_addresses:
#             try:
#                 stub = database_grpc.BookDatabaseStub(grpc.insecure_channel(address))
#                 stub.UpdateSlave(database.BookWrite(title=request.title, newStock=request.newStock))
#                 print(f"Updated slave for {request.title}")
#             except grpc.RpcError as e:
#                 print(f"Failed to update slave: {e}")
#                 success = False
#         return success

# def serve():
#     server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#     service = BookDatabaseService()
#     database_grpc.add_BookDatabaseServicer_to_server(service, server)
    
#     # Use the port from environment or a default
#     listening_port = os.getenv("LISTENING_PORT", "50057")
#     server.add_insecure_port(f'[::]:{listening_port}')
#     server.start()
#     print(f"Server started on port {listening_port}")
#     server.wait_for_termination()

# if __name__ == '__main__':
#     serve()



class BookDatabaseService(database_grpc.BookDatabaseServicer):
    def __init__(self):
        self.book_stock = {}  # Start with an empty dictionary
        self.is_master = os.getenv("IS_MASTER", "false").lower() == 'true'
        self.initialize_book_stock()

    def initialize_book_stock(self):
        books_data = {
            "Learning Python": 7,
            "JavaScript - The Good Parts": 15
        }
        self.book_stock.update(books_data)
        print("Book stock initialized:", self.book_stock)

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
            return database.UpdateAck(success=True, message="Stock updated successfully.")
        return database.UpdateAck(success=False, message="Write operation not allowed on slave.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    service = BookDatabaseService()
    database_grpc.add_BookDatabaseServicer_to_server(service, server)
    port = os.getenv("LISTENING_PORT", "50057")
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Server started on port {port}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()