from flask import Flask, request, jsonify
import os
import shutil
import demo

app = Flask(__name__)

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        data = request.get_json()
        if 'image_url' not in data:
            return jsonify({'error': 'Missing image_url parameter'}), 400

        image_url = data['image_url']
        result = demo.get_result(image_url)
        final_result, errstring = result.split(" : ", 1)
        
        # Final Response
        response = {
            'result': final_result,
            'error': errstring
        }
        
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')