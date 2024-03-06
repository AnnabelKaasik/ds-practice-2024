from concurrent.futures import ThreadPoolExecutor
import os
import multiprocessing
import time

def process_order(order_data):
    # Dispatch order data to backend microservices
    # Wait for results and return them
    time.sleep(order_data)
    return f"Processed order {order_data}"

def process_order2(order_data):
    # Dispatch order data to backend microservices
    # Wait for results and return them

    return f"Processed order2 {order_data}"

# Function to handle user request
def handle_request():
    order_data = [process_order,process_order2,process_order2,process_order]

    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit tasks to the thread pool
        futures = [executor.submit(data, 1) for data in order_data]
        
        # Wait for all tasks to complete
        results = [future.result() for future in futures]

    # Aggregate results and send response to user
    return results

print(handle_request())