from flask import Flask, request, jsonify
import asyncio
from main import get_result

app = Flask(__name__)

@app.route('/process_image', methods=['POST'])
async def process_image():
    try:
        # Retrieve the JSON data from the request
        data = await request.get_json()
        base64_image = data.get('base64_image')
       
        # Check if base64_image is provided
        if not base64_image:
            return jsonify({'error': 'No base64 image provided'}), 400
       
        # Call the get_result function to process the base64 image
        final_result = await get_result(base64_image)
       
        # Prepare the response
        response = final_result
        return jsonify(response), 200
    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5001, host='0.0.0.0')