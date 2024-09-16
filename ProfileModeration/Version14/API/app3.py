# Modified by Sir

from flask import Flask, request, jsonify
from main import get_result
from multiprocessing import Process, Queue, Event
# import base64
# import io
from PIL import Image

app = Flask(__name__)

# Create a Queue and Event for managing request processing
request_queue = Queue()
processing_event = Event()

def worker():
    while True:
        # Wait for a request to be added to the queue
        processing_event.wait()
        processing_event.clear()
        
        # Process the request
        base64_image = request_queue.get()
        if base64_image is None:
            break  # Exit the worker process if None is received
        
        # Call the get_result function to process the base64 image
        final_result = get_result(base64_image)
        
        # Simulate sending back the result (e.g., write to a file, send over network)
        print(final_result)
        
def process_request(base64_image):
    # Add the request to the queue
    request_queue.put(base64_image)
    
    # Signal the worker process to start processing
    processing_event.set()

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        # Retrieve the JSON data from the request
        data = request.get_json()
        base64_image = data.get('base64_image')
        
        # Check if base64_image is provided
        if not base64_image:
            return jsonify({'error': 'No base64 image provided'}), 400
        
        # Process the request
        process_request(base64_image)
        
        # Respond to the client indicating that the request is being processed
        return jsonify({'message': 'Request is being processed'}), 202
        
    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Start the worker process
    worker_process = Process(target=worker)
    worker_process.start()
    
    # Run the Flask app
    app.run(debug=True, port=5001, host='0.0.0.0')
    
    # Ensure the worker process is terminated
    worker_process.terminate()