from flask import Flask, request, jsonify
import Test

app = Flask(__name__)

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        data = request.get_json()
        image_url = data['image_url']

        # Call the get_result function to process the image and get the result, errors, and confidence scores
        result, err, confidence_scores = Test.get_result(image_url)

        # Include the confidence scores in the JSON response
        response = {
            'result': result,
            'error': err,
            'confidence_scores': confidence_scores
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002, host='0.0.0.0')