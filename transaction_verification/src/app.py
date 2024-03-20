import datetime
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


utils_path2 = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path2)
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

import grpc
from concurrent import futures
import re

def detectFraud(data):
    # Connect to the fraud detection service.
    total_qty = data.items[0].quantity
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        # Create a stub object.
        stub = fraud_detection_grpc.FraudDetectionServiceStub(channel)
        # Call the service through the stub object.
        response = stub.FraudDetection(fraud_detection.FraudRequest(total_qty=total_qty))
        if response.is_valid:
            return transaction_verification.VerifyTransactionResponse(is_valid=True)
        else:
            return transaction_verification.VerifyTransactionResponse(is_valid=False, error_message="Transaction is fraud")

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
        
        
        current_year, current_month = datetime.datetime.today().year, datetime.datetime.today().month
        expiration_date = request.transaction.credit_card.expirationDate

        expiration_month, expiration_year = map(int, expiration_date.split('/'))
        expiration_year += 2000  # Year to correct format

        # Check if credit card expiration month correctness
        if  expiration_month > 12:
            return transaction_verification.VerifyTransactionResponse(is_valid=False, error_message="Invalid credit card expiration date.")
        # Check if credit card is expired
        if  (expiration_year, expiration_month) < (current_year, current_month):
            return transaction_verification.VerifyTransactionResponse(is_valid=False, error_message="Credit card is expired or .")
        try:
            print("LOG: Transaction verification service called fraud detection service.")
            return detectFraud(request.transaction)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Error: ' + str(e))
            return transaction_verification.VerifyTransactionResponse(is_valid=False, error_message='Error: ' + str(e))


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