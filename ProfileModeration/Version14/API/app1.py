# Modified by Sir

from flask import Flask, request, jsonify
from threading import Thread
from main import get_result

app = Flask(__name__)

def process_image_in_thread(base64_image, callback):
    try:
        # Call the get_result function to process the base64 image
        final_result = get_result(base64_image)
        print(final_result)
        # Call the callback function with the result
        callback({'result': final_result})
    except Exception as e:
        # Call the callback function with the error
        callback({'error': str(e)})

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        # Retrieve the JSON data from the request
        data = request.get_json()
        base64_image = data.get('base64_image')

        # Check if base64_image is provided
        if not base64_image:
            return jsonify({'error': 'No base64 image provided'}), 400

        # Create a dictionary to hold the result
        result = {'result': None, 'error': None}

        # Define a callback function to update the result
        def callback(response):
            result.update(response)

        # Start a new thread to process the image
        thread = Thread(target=process_image_in_thread, args=(base64_image, callback))
        thread.start()
        thread.join()  # Wait for the thread to finish

        # Prepare the response
        if result['error']:
            return jsonify({'error': result['error']}), 500
        return jsonify(result['result']), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5001, host='0.0.0.0')