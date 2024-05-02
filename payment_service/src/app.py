import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/payment_service'))
sys.path.insert(0, utils_path)
import payment_service_pb2 as payment_service
import payment_service_pb2_grpc as payment_service_grpc

import grpc
from concurrent import futures

        

class PaymentService(payment_service_grpc.PaymentServiceServicer):
    def ProcessPayment(self, request, context):
        print("LOG: Payment service called.", request.orderId)
        if request.commit:
            print("LOG: Payment processed successfully.")
            return payment_service.PaymentResponse(orderId = request.orderId, success = True ,message="Payment processed successfully and committed.")
        return payment_service.PaymentResponse(orderId = request.orderId, success = True ,message="Payment processed successfully, not committed.")
        # return response


def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    payment_service_grpc.add_PaymentServiceServicer_to_server(PaymentService(), server)
    # Listen on port 50051
    port = "50060"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Server started. Listening on port 50060.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()