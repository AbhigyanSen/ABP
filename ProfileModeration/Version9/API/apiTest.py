from flask import Flask, request, jsonify
import base64
import Test

app = Flask(__name__)

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        data = request.get_json()
        base64_str = data['image_base64']
        
        # Call the get_result function to process the image and get the result, errors, and confidence scores
        result, err = Test.get_result(base64_str)

        return jsonify({'result': result, 'error': err}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')