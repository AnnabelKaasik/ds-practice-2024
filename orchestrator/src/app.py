import sys
import os
from concurrent.futures import ThreadPoolExecutor
from jsonschema import validate
import json

from utils.pb.transaction_verification.transaction_verification_pb2 import VectorClock
from utils.pb.suggestions_service.suggestions_service_pb2 import VectorClock

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


def verify_transaction(transaction_data, vector_clock):
    print('trying to verify transaction', vector_clock)
    vector_clock.clock['transaction_verification'] += 1
    print(f"LOG: verctor clock updated: {vector_clock}")
    # Connects to transaction verification service and sends the data to verification
    with grpc.insecure_channel('transaction_verification:50052') as channel:
        stub = transaction_verification_grpc.TransactionVerificationServiceStub(channel)
        
        #if the items is not a list, convert it to a list
        if type(transaction_data["items"]) == dict:
            transaction_data["items"] = [transaction_data["items"]]
        
        # print(f"LOG: Transaction data: {transaction_data}")
        
        # Make data suitable for proto file
        transaction_data = transaction_verification.Transaction(
            items=[transaction_verification.Item(
                bookid=item['id'],
                quantity=item['quantity']
            ) for item in transaction_data['items']],
            user=transaction_verification.User(
                name=transaction_data['user']['name'],
                contact=transaction_data['user']['contact']
            ),
            credit_card=transaction_verification.CreditCard(
                number=transaction_data['creditCard']['number'],
                expirationDate=transaction_data['creditCard']['expirationDate'],
                cvv=transaction_data['creditCard']['cvv']
            )
            )
        
        # verification request
        print(f"LOG: before response")
        response = stub.VerifyTransaction(transaction_verification.VerifyTransactionRequest(
            transaction=transaction_data, 
            vector_clock = transaction_verification.VectorClock(clock=vector_clock.clock)))
        print(f"LOG: after response")
        return response
    


def getBookSuggestions(data, vector_clock):
    # print('book suggestions', vector_clock)
    vector_clock.clock['suggestions_service'] += 1
    # print(f"LOG: verctor clock updated: {vector_clock}")
    id = data['items'][0]['id']
    with grpc.insecure_channel('suggestions_service:50053') as channel:
        # Create a stub object.
        stub = suggestions_service_grpc.SuggestionsServiceStub(channel)
        # Call the service through the stub object.
        try:
            # print(f"LOG: before response")
            request = suggestions_service.getSuggestionsRequest(
                bookid=id, 
                vector_clock=suggestions_service.VectorClock(clock=vector_clock.clock))
            response = stub.getSuggestions(request)
            #  this gets printed, prblem needs to be inside the respone.
            # print(f"LOG: after response")
        except Exception as e:
            print(f"ERROR: Exception in getBookSuggestions: {e}")
            # Should I do this here???
            return {"error": {"code": "500","message": "Internal Server Error"}}, 500

    return response.items, response.vector_clock




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
    print("Log: Received a GET request")
    response = 'Hello, World!'
    # Return the response.
    return response

@app.route('/checkout', methods=['POST'])
def checkout():
    """
    Responds with a JSON object containing the order ID, status, and suggested books.
    """
    vector_clock = VectorClock(clock = {'transaction_verification': 0, 'fraud_detection': 0, 'suggestions_service': 0})
    
    print("LOG: Recieved a POST request on /checkour endpoint")
    data = request.json
    print(f"LOG: Request data: {data}")

    
    with open('orchestrator/src/schema.json') as f:
        schema = json.load(f)
        
    try:
        validate(instance=data, schema=schema)
    except Exception as e:
        print(f"LOG: Schema validation failed: {e}")
        return {"error": {"code": "400","message": f"Schema validation failed: {e}"}}, 400
    

    # functions = [verify_transaction, getBookSuggestions]
    
    
    # NOT ORDERED LAST SOLUTION

    # try:
    #     print("LOG: Starting paralles processing of microservices")
    #     with ThreadPoolExecutor(max_workers=2) as executor:
    #         # Submit tasks to the thread pool
    #         futures = [executor.submit(f, data) for f in functions]
            
    #         # Wait for all tasks to complete
    #         verification_response, book_suggestions = [future.result() for future in futures]
    # except Exception as e:
    #     print(f"LOG: Error during paralles processing of microservices {e}")
    #     return {"error": {"code": "500","message": "Internal Server Error"}}, 500



    # print(f"LOG: Verification and fraud Response: {verification_response}")
    # print(f"LOG: Book Suggestions: {book_suggestions}")

    # if verification_response.is_valid:
    #     order_status_response = {
    #     'orderId': '12345',
    #     'status': "Order Approved",
    #     'suggestedBooks': [
    #     {'bookId': book.bookid, 'title': book.title, 'author': book.author}
    #     for book in book_suggestions
    # ]
    # }
    # else:
    #     order_status_response = {
    #     'orderId': '12345',
    #     'status': "Order Rejected"
    # }
    
    # print(f"LOG: Final response: {order_status_response}")

    # NEW VECTOR CLOCK SOLUTION
    # Commented out verification_response for easier testing with book sugeestion
    try:
        print('trying hardest', vector_clock)
        verification_response, vector_clock = verify_transaction(data, vector_clock)
        print(f"LOG: Verification and Fraud Response: {verification_response}, {vector_clock}")

        if verification_response.is_valid:
            book_suggestions, vector_clock = getBookSuggestions(data, vector_clock)
            print(f"LOG: Book Suggestions in orc: {book_suggestions}, {vector_clock}")
            order_status_response = {
                'orderId': '12345',
                'status': "Order Approved",
                'suggestedBooks': [
                {'bookId': book.bookid, 'title': book.title, 'author': book.author}
                for book in book_suggestions
                ]
            }
        else:
            order_status_response = {
            'orderId': '12345',
            'status': "Order Rejected"
        }
    except Exception as e:
        return {"error": {"code": "500","message": "Internal Server Error"}}, 500

    return order_status_response, 200


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')
