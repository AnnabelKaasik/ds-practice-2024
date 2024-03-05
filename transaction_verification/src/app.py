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
        
        # Check for user name and contact
        if not request.transaction.user or not request.transaction.user.name or not request.transaction.user.contact:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Missing user name or contact')
            return transaction_verification.VerifyTransactionResponse(is_valid=False, error_message='Missing user name or contact')
        # Check is credit card number is 16 digits
        if not re.match(r'^[0-9]{16}$', request.transaction.credit_card.number): 
            return transaction_verification.VerifyTransactionResponse(is_valid=False, error_message="Invalid credit card number.")
        return transaction_verification.VerifyTransactionResponse(is_valid=True)


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