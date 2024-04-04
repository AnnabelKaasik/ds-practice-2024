import sys
import os
import json

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions_service'))
sys.path.insert(0, utils_path)
import suggestions_service_pb2 as suggestions_service
import suggestions_service_pb2_grpc as suggestions_service_grpc

import grpc
from concurrent import futures

books = {"1":{"title":"Learning Python","author":"John Smith"},
         "2":{"title":"JavaScript - The Good Parts","author":"Jane Doe"},
         "3":{"title":"Domain-Driven Design: Tackling Complexity in the Heart of Software","author":"Eric Evans"},
         "4":{"title":"Design Patterns: Elements of Reusable Object-Oriented Software","author":"Erich Gamma, Richard Helm, Ralph Johnson, & John Vlissides"}
         }



class SuggestionsService(suggestions_service_grpc.SuggestionsServiceServicer):
    
    def getSuggestions(self, request, context):
        print("LOG: Suggestions service called.")
        request.vector_clock.clock['suggestions_service'] += 1
        
        suggestions = [i for i in books if request.bookid != i]
        
        response = []
        for i in suggestions[:3]:
            response.append(suggestions_service.Book(bookid = i, title=books[i]["title"], author=books[i]["author"]))
            
        print("LOG: Suggestions service finished.")
        request.vector_clock.clock['suggestions_service'] += 1
        return suggestions_service.SuggestionsResponse(items=response, vector_clock = request.vector_clock)
        
    

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    suggestions_service_grpc.add_SuggestionsServiceServicer_to_server(SuggestionsService(), server)
    # Listen on port 50053
    port = "50053"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Server started. Listening on port 50053.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()