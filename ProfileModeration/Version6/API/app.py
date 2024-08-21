from flask import Flask, request, jsonify
import demo

app = Flask(__name__)

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        data = request.get_json()
        image_url = data['image_url']

        result,err = demo.get_result(image_url)

        return jsonify({'result': result,"error":err}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001,host='0.0.0.0')