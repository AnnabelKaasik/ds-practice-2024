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

from utils.pb.fraud_detection.fraud_detection_pb2 import VectorClock

def detectFraud(data, vector_clock):
    vector_clock.clock['fraud_detection'] += 1
    print(f"LOG: Fraud detection vector clock updated: {vector_clock}")
    # Connect to the fraud detection service.
    total_qty = data.items[0].quantity
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        # Create a stub object.
        stub = fraud_detection_grpc.FraudDetectionServiceStub(channel)
        # Call the service through the stub object.
        try:
            response = stub.FraudDetection(fraud_detection.FraudRequest(total_qty=total_qty))
            if response.is_valid:
                print("LOG: Transaction is valid.")
                return transaction_verification.VerifyTransactionResponse(is_valid=True)
            else:
                return transaction_verification.VerifyTransactionResponse(is_valid=False, 
                                                                        error_message="Transaction is fraud", 
                                                                        vector_clock = fraud_detection.VectorClock(clock=vector_clock.clock))
        except Exception as e:
            print(f"ERROR: Exception in detectFraud: {e}")


class TransactionVerificationService(transaction_verification_grpc.TransactionVerificationServiceServicer):
    def VerifyTransaction(self, request, context):
        print("LOG: Transaction verification service called.", request.vector_clock)
        request.vector_clock.clock['transaction_verification'] += 1
        print("LOG: Transaction verification vector clock updated: ", request.vector_clock)
        
        # Check for user name and contact
        if not request.transaction.user or not request.transaction.user.name or not request.transaction.user.contact:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Missing user name or contact')
            # maybe shuld change how vector clock is passed
            return transaction_verification.VerifyTransactionResponse(is_valid=False, error_message='Missing user name or contact', vector_clock = request.vector_clock)
        print("LOG: Transaction verification service user name and contact verified.")
        # Check is credit card number is 16 digits
        if not re.match(r'^[0-9]{16}$', request.transaction.credit_card.number): 
            return transaction_verification.VerifyTransactionResponse(is_valid=False, error_message="Invalid credit card number.", vector_clock = request.vector_clock)
        print("LOG: Transaction verification service credit card number verified.")
        
        current_year, current_month = datetime.datetime.today().year, datetime.datetime.today().month
        expiration_date = request.transaction.credit_card.expirationDate

        expiration_month, expiration_year = map(int, expiration_date.split('/'))
        expiration_year += 2000  # Year to correct format

        # Check if credit card expiration month correctness
        if  expiration_month > 12:
            return transaction_verification.VerifyTransactionResponse(is_valid=False, error_message="Invalid credit card expiration date.", vector_clock = request.vector_clock)
        print("LOG: Transaction verification service credit card expiration month verified.")
        # Check if credit card is expired
        if  (expiration_year, expiration_month) < (current_year, current_month):
            return transaction_verification.VerifyTransactionResponse(is_valid=False, error_message="Credit card is expired or .", vector_clock = request.vector_clock)
        print("LOG: Transaction verification service credit card expiration date verified.")
        

        try:
            print("LOG: Transaction verification service called fraud detection service.")

            fraud_response, vector_clock = detectFraud(request.transaction, request.vector_clock)
            return transaction_verification.VerifyTransactionResponse(is_valid=fraud_response.is_valid, error_message=fraud_response.message, vector_clock = request.vector_clock)
        
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Error: ' + str(e))
            return transaction_verification.VerifyTransactionResponse(is_valid=False, error_message='Error: ' + str(e), vector_clock = request.vector_clock)


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