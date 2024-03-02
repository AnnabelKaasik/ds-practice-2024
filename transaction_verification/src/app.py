import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, utils_path)
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

import grpc
from concurrent import futures
import re



class TransactionVerificationService(transaction_verification_grpc.TransactionVerificationServiceServicer):
    def VerifyTransaction(self, request, context):
        # print("Request received:", request)
        # print(" plaplapla")
        # print("User Name:", request.user.name)
        # print("User Contact:", request.user.contact)

        if not request.user or not request.user.name or not request.user.contact:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Missing user name or contact')
            return transaction_verification.VerifyTransactionResponse(is_valid=False, error_message='Missing user name or contact')
        if not re.match(r'^[0-9]{16}$', request.credit_card.number): 
            return transaction_verification.VerifyTransactionResponse(is_valid=False, error_message="Invalid credit card number.")
        return transaction_verification.VerifyTransactionResponse(is_valid=True)


# # Create a class to define the server functions, derived from
# # fraud_detection_pb2_grpc.HelloServiceServicer
# class HelloService(transaction_verification_grpc.HelloServiceServicer):
#     # Create an RPC function to say hello
#     def SayHello(self, request, context):
#         # Create a HelloResponse object
#         response = transaction_verification.HelloResponse()
#         # Set the greeting field of the response object
#         response.greeting = "Hello, " + request.name
#         # Print the greeting message
#         print(response.greeting)
#         # Return the response object
#         return response

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add ransactionVerificationService
    transaction_verification_grpc.add_TransactionVerificationServiceServicer_to_server(TransactionVerificationService(), server)
    # Listen on port 50052
    port = "50052"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Server started. Listening on port 50052.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()