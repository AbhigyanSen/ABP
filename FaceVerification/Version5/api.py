from flask import Flask, request, jsonify
from main import process_images
from FaceMatching import compareFace2Aadhar
app = Flask(__name__)

@app.route('/matchFace', methods=['POST'])
def process_face():
    # Parse the JSON body from the request
    data = request.get_json()
    
    # Extract values from the JSON
    face1 = data.get('face1')
    face2 = data.get('face2')
    
    # Simple validation
    if face1 is None or face2 is None:
        return jsonify({"error": "Missing value1 or value2"}), 400
    
    # Example processing: add the two values
    result = compareFace2Aadhar(face1,face2)
    
    # Return the result as JSON
    return jsonify({"result": result})

@app.route('/processDocument', methods=['POST'])
def process_document():
    # Parse the JSON body from the request
    data = request.get_json()
    
    # Extract values from the JSON
    face = data.get('face')
    document = data.get('document')
    
    # Simple validation
    if face is None or document is None:
        return jsonify({"error": "Missing value1 or value2"}), 400
    
    # Example processing: add the two values
    result = process_images(face,document)
    
    # Return the result as JSON
    return jsonify({"result": result})



if __name__ == '__main__':
    app.run(debug=True,port=5002, host='0.0.0.0')
