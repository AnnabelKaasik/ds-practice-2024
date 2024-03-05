import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path)
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc


utils_path2 = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions_service'))
sys.path.insert(0, utils_path2)
import suggestions_service_pb2 as suggestions_service
import suggestions_service_pb2_grpc as suggestions_service_grpc


utils_path3 = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, utils_path3)
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

import grpc


def verify_transaction(transaction_data):
    
    
    try: 
        required_fields = [
            # 'user', 
            'creditCard', 'items', 'termsAndConditionsAccepted']
        missing_fields = [field for field in required_fields if field not in transaction_data]
        if missing_fields:
            return {'is_valid': False, 'error_message': 'Missing required fields: ' + ', '.join(missing_fields)}

    # Connects to transaction verification service and sends the data to verification
        with grpc.insecure_channel('transaction_verification:50052') as channel:
            stub = transaction_verification_grpc.TransactionVerificationServiceStub(channel)

            # Make data suitable for proto file
            transaction = transaction_verification.Transaction(
                user=transaction_verification.User(
                    name=transaction_data['user']['name'],
                    contact=transaction_data['user']['contact']
                ),
                credit_card=transaction_verification.CreditCard(
                    number=transaction_data['creditCard']['number'],
                    expirationDate=transaction_data['creditCard']['expirationDate'],
                    cvv=transaction_data['creditCard']['cvv']
                ),
                items=[
                    transaction_verification.Item(name=item['name'], quantity=item['quantity'])
                    for item in transaction_data.get('items', [])
                ],
                terms_and_conditions_accepted=transaction_data['termsAndConditionsAccepted'],
            )
            
            # verification request
            request = transaction_verification.VerifyTransactionRequest(transaction=transaction)
            response = stub.VerifyTransaction(request)
            return {'is_valid': response.is_valid, 'error_message': response.error_message if not response.is_valid else ''}
        
    except Exception as e:
        # Handle unexpected errors
        return {'is_valid': False, 'error_message': 'An error occurred during processing: ' + str(e)}



def getBookSuggestions(id):
    with grpc.insecure_channel('suggestions_service:50053') as channel:
        # Create a stub object.
        stub = suggestions_service_grpc.SuggestionsServiceStub(channel)
        # Call the service through the stub object.
        response = stub.getSuggestions(suggestions_service.getSuggestionsRequest(bookid = id))
    return response.items


def detectFraud(total_qty):
    # Connect to the fraud detection service.
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        # Create a stub object.
        stub = fraud_detection_grpc.FraudDetectionServiceStub(channel)
        # Call the service through the stub object.
        response = stub.FraudDetection(fraud_detection.FraudRequest(total_qty=total_qty))
    return response.message


# Import Flask.
# Flask is a web framework for Python.
# It allows you to build a web application quickly.
# For more information, see https://flask.palletsprojects.com/en/latest/
from flask import Flask, request, jsonify
from flask_cors import CORS

# Create a simple Flask app.
app = Flask(__name__)
# Enable CORS for the app.
CORS(app)

# Define a GET endpoint.
@app.route('/', methods=['GET'])
def index():
    """
    Responds with 'Hello, [name]' when a GET request is made to '/' endpoint.
    """
    response = 'Hello, World!'
    # Return the response.
    return response

@app.route('/checkout', methods=['POST'])
def checkout():
    """
    Responds with a JSON object containing the order ID, status, and suggested books.
    """

    data = request.json
    # Print request object data
    print("Request Data:", request.json)

    verification_response = verify_transaction(data)
    print(verification_response)
    print(getBookSuggestions(data['items'][0]['id']))
    print(detectFraud(data['items'][0]['quantity']))

    if verification_response["is_valid"]:
        order_status_response = {
        'orderId': '12345',
        'status': "Order Approved",
        'suggestedBooks': [
            {'bookId': '123', 'title': 'Dummy Book 1', 'author': 'Author 1'},
            {'bookId': '456', 'title': 'Dummy Book 2', 'author': 'Author 2'}
        ]
    }
    else:
        order_status_response = {
        'orderId': '12345',
        'status': "Order Rejected",
        'suggestedBooks': [
            {'bookId': '123', 'title': 'Dummy Book 1', 'author': 'Author 1'},
            {'bookId': '456', 'title': 'Dummy Book 2', 'author': 'Author 2'}
        ]
    }
    # Dummy response following the provided YAML specification for the bookstore
    # order_status_response = {
    #     'orderId': '12345',
    #     'status': "",
    #     'suggestedBooks': [
    #         {'bookId': '123', 'title': 'Dummy Book 1', 'author': 'Author 1'},
    #         {'bookId': '456', 'title': 'Dummy Book 2', 'author': 'Author 2'}
    #     ]
    # }
    print(order_status_response)
    return jsonify(order_status_response)


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')
