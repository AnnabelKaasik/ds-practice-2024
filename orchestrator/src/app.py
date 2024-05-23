import sys
import os
from concurrent.futures import ThreadPoolExecutor
from jsonschema import validate
import json
from multiprocessing import Value

from utils.pb.transaction_verification.transaction_verification_pb2 import VectorClock
from utils.pb.suggestions_service.suggestions_service_pb2 import VectorClock


from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# Service name is required for most backends
resource = Resource(attributes={
    SERVICE_NAME: "observability"
})

traceProvider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://observability:4318/v1/traces"))
traceProvider.add_span_processor(processor)
trace.set_tracer_provider(traceProvider)

reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://observability:4318/v1/metrics")
)
meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meterProvider)

meter = metrics.get_meter("orchestrator")
counter1 = meter.create_counter(name="total.orders.started", description="Total number of orders started")
counter2 = meter.create_counter(name="total.orders.sent.to.queue", description="Total number of orders sent to queue")

counter3 = meter.create_up_down_counter(
        name="total.books.sold", description="Total books sold",
    )

tracer = trace.get_tracer("traces.form.orchestrator")
histogram = meter.create_histogram(
        name="average.order.size",
        description="average order size",
        unit="books",
    )


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

utils_path4 = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_queue'))
sys.path.insert(0, utils_path4)
import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc

import grpc
order_id_count = Value('i', 0)

def enqueue_order(order_id, order_data):
    # Connects to order queue service and sends the data to queue
    print(f"LOG: Enqueueing order: {order_id}")
    try:
        with grpc.insecure_channel('order_queue:50054') as channel:
            stub = order_queue_grpc.OrderQueueServiceStub(channel)
            order_message = order_queue.Order(
                orderId=str(order_id), 
                userName=order_data['user']['name'],
                # Added booktitle and quantity
                bookTitle=order_data['items'][0]['name'],
                quantity=order_data['items'][0]['quantity'])
            response = stub.EnqueueOrder(order_queue.EnqueueRequest(order=order_message))
            print(f"LOG: Order enqueued: {response}")
            
    except Exception as e:
        print(f"ERROR: Exception in enqueue_order: {e}")
        return {"error": {"code": "500","message": "Internal Server Error"}}, 500

    return response
    

def verify_transaction(transaction_data, vector_clock):
    # Connects to transaction verification service and sends the data to verify
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
        try:
            response = stub.VerifyTransaction(transaction_verification.VerifyTransactionRequest(
                transaction=transaction_data, 
                vector_clock = transaction_verification.VectorClock(clock=vector_clock.clock)))
        except Exception as e:
            print(f"ERROR: Exception in verify_transaction: {e}")
            return {"error": {"code": "500","message": f"Internal Server Error {e}"}}, 500
        print(f"LOG: after response")
        return response
    


def getBookSuggestions(data, vector_clock):

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
            return {"error": {"code": "500","message": "Internal Server Error"}}, 500
    

    return response




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
    counter1.add(1)
    with tracer.start_as_current_span("new_order") as span:
        span.set_attribute("data", str(request.json))
    
    """
    Responds with a JSON object containing the order ID, status, and suggested books.
    """
    with order_id_count.get_lock():
        vector_clock = VectorClock(clock = {'order_id': order_id_count.value,
                                            'transaction_verification': 0,
                                            'fraud_detection': 0,
                                            'suggestions_service': 0,
                                            'orchestrator': 1,})
        order_id_count.value += 1
    
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
    

    try:

        functions = [verify_transaction, getBookSuggestions]
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(f, data, vector_clock) for f in functions]
            verification_response, book_suggestions_response = [future.result() for future in futures]
            
        for key in verification_response.vector_clock.clock.keys():
            vector_clock.clock[key] = max(verification_response.vector_clock.clock[key], book_suggestions_response.vector_clock.clock[key])
        
        vector_clock.clock['orchestrator'] += 1
        print(f"LOG: Vector clock: {vector_clock}")

        if verification_response.is_valid:
            queue_response = enqueue_order(vector_clock.clock['order_id'], data)
            if queue_response.success:
                order_status_response = {
                    'orderId': vector_clock.clock['order_id'],
                    'status': "Order Approved",
                    'suggestedBooks': [
                    {'bookId': book.bookid, 'title': book.title, 'author': book.author}
                    for book in book_suggestions_response.items
                    ]
                }
                counter2.add(1)
                number_of_books = [int(item['quantity']) for item in data['items']]
                counter3.add(sum(number_of_books))
                histogram.record(sum(number_of_books)*10)
            else:
                order_status_response = {
                    'orderId': vector_clock.clock['order_id'],
                    'status': "We were unable to process your order. Please try again later."
                }
        else:
            order_status_response = {
            'orderId': vector_clock.clock['order_id'],
            'status': "Order Rejected"
        }
    except Exception as e:
        print(f"LOG: Error during paralles processing of microservices {e}")
        return {"error": {"code": "500","message": "Internal Server Error"}}, 500
       

    return order_status_response, 200


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')
